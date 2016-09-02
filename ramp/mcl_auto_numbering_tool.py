# -*- coding: utf-8 -*-
from copy import copy

from qgis.core import QgsFeatureRequest, QgsExpression
from qgis.gui import QgsMessageBar

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialogButtonBox
from PyQt4.QtSql import QSqlQuery
from Roadnet.roadnet_dialog import RampMclAutoNumberingDlg
import Roadnet.roadnet_exceptions as rn_except
from Roadnet.generic_functions import ipdb_breakpoint


class MclAutoNumberingTool(object):
    """
    Allows user to select MCL segments, then updates their segment numbers
    """
    dlg = None
    current_mcls = []

    def __init__(self, mcl, db, iface):
        """
        Prepare numbering tool
        :param mcl: QgsVectorLayer for MCL layer
        :param db: open QSqlDatabase
        :param iface: QGIS interface
        """
        self.mcl = mcl
        self.db = db
        self.iface = iface
        self.prepare_dialog()
        self.connect_signals()

    def prepare_dialog(self):
        """
        Create dialog, including setting initial defaults
        """
        # Prepare dialog
        self.dlg = RampMclAutoNumberingDlg()
        self.dlg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.dlg.move(5, 5)

        # Set initial values
        self.dlg.ui.startValueSpinBox.setMaximum(9999)
        self.dlg.ui.incrementSpinBox.setValue(10)
        self.mcl.removeSelection()
        self.update_mcl_sections_box()

    def connect_signals(self):
        """
        Connect GUI signals and slots.  Extends parent class function
        """
        self.mcl.selectionChanged.connect(self.update_mcl_sections_box)
        # GUI controls
        ok_button = self.dlg.ui.buttonBox.button(QDialogButtonBox.Ok)
        cancel_button = self.dlg.ui.buttonBox.button(QDialogButtonBox.Cancel)
        ok_button.clicked.connect(self.apply)
        cancel_button.clicked.connect(self.close_tool)
        # reject() is called if user presses escape
        self.dlg.rejected.connect(self.close_tool)

    def apply(self):
        """
        Apply changes to database
        """
        self.number_mcls()
        self.close_tool()

    def number_mcls(self):
        """
        Update the database with numbered MCL sections then close dialog
        """
        mcl_refs, start_value, increment = self.get_dialog_values()

        mcl_number = start_value
        for mcl_ref in mcl_refs:
            self.set_db_mcl_number(mcl_ref, mcl_number)
            mcl_number += increment

    def get_dialog_values(self):
        """
        Get the current values from the dialog.
        :return mcl_refs: list of strings
        :return start_value: int
        :return increment: int
        """
        mcl_box = self.dlg.ui.mclListWidget
        mcl_refs = [mcl_box.item(x).text() for x in range(mcl_box.count())]
        start_value = self.dlg.ui.startValueSpinBox.value()
        increment = self.dlg.ui.incrementSpinBox.value()

        return mcl_refs, start_value, increment

    def set_db_mcl_number(self, mcl_ref, mcl_number):
        """
        Update database with new MCL number
        :param mcl_ref:
        :param mcl_number:
        """
        sql = """
            UPDATE mcl SET lor_ref_2 = {mcl_number}
            WHERE mcl_ref = {mcl_ref}
            ;""".format(mcl_ref=mcl_ref, mcl_number=mcl_number)
        query = QSqlQuery(sql, self.db)

        rows_affected = query.numRowsAffected()
        if rows_affected != 1:
            msg = "Error in setting MCL number."
            msg += "\nQuery:\n{}".format(sql)
            msg += "\nRows affected: {}".format(rows_affected)
            msg += "\nDatabase said:\n{}".format(query.lastError().text())
            raise rn_except.RampMclNumberingFailedPopupError(msg)

    def update_mcl_sections_box(self):
        """
        Update the selected MCLs box with the newly selected feature, preserving
        selection order from previous selection.
        """
        selected_features = self.mcl.selectedFeatures()
        selected_mcls = [str(feature['mcl_ref'])
                         for feature in selected_features]

        if selected_features:
            current_mcls = self.update_current_mcls(selected_mcls)
        else:
            current_mcls = []

        # Update gui and store values for next time
        self.populate_mcl_sections_box(current_mcls)
        self.current_mcls = current_mcls
        self.iface.mapCanvas().refresh()

    def update_current_mcls(self, selected_mcls):
        """
        Update list of MCLs to process.  Append or remove new selections to
        keep list in order of selection.  Otherwise items are listed in PK_UID
        order.
        :param selected_mcls: list of str mcl_refs
        :return current_mcls: list of str
        """
        current_mcls = copy(self.current_mcls)
        added_mcls = [mcl for mcl in selected_mcls
                      if mcl not in current_mcls]
        removed_mcls = [mcl for mcl in current_mcls
                        if mcl not in selected_mcls]

        # Only allow features to be added one at a time
        if len(added_mcls) not in (0, 1):
            # Show warning
            changed_mcl_count = len(added_mcls + removed_mcls)
            self.warn_and_revert_selection(changed_mcl_count, current_mcls)
            return current_mcls

        if added_mcls:
            # Append newly selected MCL to list (use extend because we have list)
            current_mcls.extend(added_mcls)

        if removed_mcls:
            # Remove unselected MCLs from list (MCL is single item in list)
            for mcl in removed_mcls:
                current_mcls.remove(mcl)

        return current_mcls

    def warn_and_revert_selection(self, changed_mcl_count, current_mcls):
        """
        Show warning to user and revert their selection to previous
        :param changed_mcl_count: int, number of MCLs changed
        :param current_mcls: list of str, mcl_refs
        """
        warning = (
            "Selection changed by {} features.  "
            "Add/remove MCLs one at a time.".format(changed_mcl_count))
        self.iface.messageBar().pushMessage('roadNet', warning,
                                            QgsMessageBar.WARNING, 3)

        # Revert selection (don't fire selection changed signal)
        self.mcl.selectionChanged.disconnect()
        self.select_mcls(current_mcls)
        self.mcl.selectionChanged.connect(self.update_mcl_sections_box)

    def select_mcls(self, mcls):
        """
        Update the selected features using mcl_ref values
        :param mcls: list of str mcl_refs
        """
        mcls_text = ', '.join(mcls)
        expression = QgsExpression("mcl_ref IN ({})".format(mcls_text))
        request = QgsFeatureRequest(expression)
        mcls_ids = [f.id() for f in self.mcl.getFeatures(request)]
        self.mcl.setSelectedFeatures(mcls_ids)

    def populate_mcl_sections_box(self, items):
        """
        Populate the Linked Polygons box with items
        :param items: list of strings
        """
        poly_box = self.dlg.ui.mclListWidget
        poly_box.clear()
        poly_box.addItems(items)

    def launch(self):
        """
        Open dialog and activate selection tool
        """
        self.iface.actionSelect().trigger()
        self.dlg.show()

    def close_tool(self):
        """
        Close dialog, and reselect previous tool
        """
        self.dlg.close()
        try:
            self.mcl.selectionChanged.disconnect(self.update_mcl_sections_box)
        except TypeError:
            pass  # this sometimes throws when changing tools
        self.iface.actionSelect().trigger()
        self.iface.mapCanvas().refresh()
