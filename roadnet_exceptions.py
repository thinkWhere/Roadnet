# -*- coding: utf-8 -*-
from PyQt4.QtGui import QMessageBox
from PyQt4.Qt import Qt
from PyQt4.QtSql import QSqlError


class QMessageBoxWarningError(Exception):
    """
    Exception that raises message box with information for user.
    """
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(QMessageBoxWarningError, self).__init__(message)
        self.show_message_box()

    def show_message_box(self):
        """
        Show message box with message.
        """
        msg_box = QMessageBox(QMessageBox.Warning, " ", self.message,
                              QMessageBox.Ok, None)
        msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        msg_box.exec_()


class MissingParamsFilePopupError(QMessageBoxWarningError):
    pass


class InvalidParamsKeysPopupError(QMessageBoxWarningError):
    pass


class ExtraParamsKeysPopupError(QMessageBoxWarningError):
    pass


class InvalidLayerPopupError(QMessageBoxWarningError):
    pass


class InvalidStylePopupError(QMessageBoxWarningError):
    pass


class CannotOpenShapefilePopupError(QMessageBoxWarningError):
    pass


class BadSpatialiteVersionPopupError(QMessageBoxWarningError):
    pass


class RemoveNonExistentLayerPopupError(QMessageBoxWarningError):
    pass


class BadRampTableStructureError(QMessageBoxWarningError):
    pass


class RampRdPolyUpdateFailedPopupError(QMessageBoxWarningError):
    pass


class RampRdPolyAlreadyLinkedPopupError(QMessageBoxWarningError):
    pass


class RampMclNumberingFailedPopupError(QMessageBoxWarningError):
    pass



class RampNoLinkedPolyPopupError(QMessageBoxWarningError):
    pass


class NoFeaturesFoundException(BaseException):
    """
    Used to raise an exception where the database would have silently
    returned nothing.
    """
    pass


class MclFormLengthCalculationError(BaseException):
    pass


class MclFormBadMclRefError(BaseException):
    pass


class RdpolyFormBadRdpolyRefError(BaseException):
    pass


class RdpolyFormBadMclRefError(BaseException):
    pass


class RdPolyNullGeometryError(BaseException):
    """
    Raised when feature in WDM export has NULL geometry.
    """
    pass


class LengthOfRoadsCalculationDatabaseError(BaseException):
    """
    Raised when Length of Roads calculation fails but database would have
    silently returned nothing.
    """
    pass


class BadSpatialiteVersionError(BaseException):
    """
    Raised with Spatialite version < 4.3.0.
    """
    pass
