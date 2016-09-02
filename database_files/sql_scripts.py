populate_layer_styles = """
INSERT INTO "layer_styles" VALUES(1,'roadnet_demo.sqlite','','rdpoly','geometry','rdpoly','<!DOCTYPE qgis PUBLIC ''http://mrcc.com/qgis.dtd'' ''SYSTEM''>
            <qgis version="2.12.3-Lyon" minimumScale="0" maximumScale="1e+08" simplifyDrawingHints="1" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0">
             <edittypes>
              <edittype widgetv2type="TextEdit" name="PK_UID">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="symbol">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="rd_pol_id">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="element">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="hierarchy">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="ref_1">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="ref_2">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="desc_1">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="desc_2">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="desc_3">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="ref_3">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="currency_flag">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="part_label">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="label">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="label1">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="feature_length">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="r_usrn">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="mcl_cref">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
             </edittypes>
             <renderer-v2 attr="SYMBOL" forceraster="0" symbollevels="0" type="categorizedSymbol">
              <categories>
               <category render="true" symbol="0" value="1" label="Unassigned"/>
               <category render="true" symbol="1" value="2" label="Multiple"/>
               <category render="true" symbol="2" value="11" label="Public"/>
               <category render="true" symbol="3" value="12" label="Prospective Public"/>
               <category render="true" symbol="4" value="13" label="Private"/>
               <category render="true" symbol="5" value="14" label="Trunk"/>
               <category render="true" symbol="6" value="" label="Default"/>
              </categories>
              <symbols>
               <symbol alpha="1" clip_to_extent="1" type="fill" name="0">
                <layer pass="0" class="SimpleFill" locked="0">
                 <prop k="border_width_map_unit_scale" v="0.0001,0,0,0,0,0"/>
                 <prop k="color" v="255,170,0,255"/>
                 <prop k="joinstyle" v="bevel"/>
                 <prop k="offset" v="0,0"/>
                 <prop k="offset_map_unit_scale" v="0.0001,0,0,0,0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="outline_color" v="228,141,59,255"/>
                 <prop k="outline_style" v="solid"/>
                 <prop k="outline_width" v="0.26"/>
                 <prop k="outline_width_unit" v="MM"/>
                 <prop k="style" v="dense4"/>
                </layer>
               </symbol>
               <symbol alpha="1" clip_to_extent="1" type="fill" name="1">
                <layer pass="0" class="SimpleFill" locked="0">
                 <prop k="border_width_map_unit_scale" v="0.0001,0,0,0,0,0"/>
                 <prop k="color" v="255,0,0,255"/>
                 <prop k="joinstyle" v="bevel"/>
                 <prop k="offset" v="0,0"/>
                 <prop k="offset_map_unit_scale" v="0.0001,0,0,0,0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="outline_color" v="227,42,57,255"/>
                 <prop k="outline_style" v="solid"/>
                 <prop k="outline_width" v="0.26"/>
                 <prop k="outline_width_unit" v="MM"/>
                 <prop k="style" v="dense5"/>
                </layer>
               </symbol>
               <symbol alpha="1" clip_to_extent="1" type="fill" name="2">
                <layer pass="0" class="SimpleFill" locked="0">
                 <prop k="border_width_map_unit_scale" v="0.0001,0,0,0,0,0"/>
                 <prop k="color" v="21,117,130,255"/>
                 <prop k="joinstyle" v="bevel"/>
                 <prop k="offset" v="0,0"/>
                 <prop k="offset_map_unit_scale" v="0.0001,0,0,0,0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="outline_color" v="21,117,130,255"/>
                 <prop k="outline_style" v="solid"/>
                 <prop k="outline_width" v="0.26"/>
                 <prop k="outline_width_unit" v="MM"/>
                 <prop k="style" v="dense4"/>
                </layer>
               </symbol>
               <symbol alpha="1" clip_to_extent="1" type="fill" name="3">
                <layer pass="0" class="SimpleFill" locked="0">
                 <prop k="border_width_map_unit_scale" v="0.0001,0,0,0,0,0"/>
                 <prop k="color" v="0,255,197,255"/>
                 <prop k="joinstyle" v="bevel"/>
                 <prop k="offset" v="0,0"/>
                 <prop k="offset_map_unit_scale" v="0.0001,0,0,0,0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="outline_color" v="42,249,208,255"/>
                 <prop k="outline_style" v="solid"/>
                 <prop k="outline_width" v="0.26"/>
                 <prop k="outline_width_unit" v="MM"/>
                 <prop k="style" v="dense4"/>
                </layer>
               </symbol>
               <symbol alpha="1" clip_to_extent="1" type="fill" name="4">
                <layer pass="0" class="SimpleFill" locked="0">
                 <prop k="border_width_map_unit_scale" v="0.0001,0,0,0,0,0"/>
                 <prop k="color" v="56,168,0,255"/>
                 <prop k="joinstyle" v="bevel"/>
                 <prop k="offset" v="0,0"/>
                 <prop k="offset_map_unit_scale" v="0.0001,0,0,0,0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="outline_color" v="51,160,44,255"/>
                 <prop k="outline_style" v="solid"/>
                 <prop k="outline_width" v="0.26"/>
                 <prop k="outline_width_unit" v="MM"/>
                 <prop k="style" v="dense4"/>
                </layer>
               </symbol>
               <symbol alpha="1" clip_to_extent="1" type="fill" name="5">
                <layer pass="0" class="SimpleFill" locked="0">
                 <prop k="border_width_map_unit_scale" v="0.0001,0,0,0,0,0"/>
                 <prop k="color" v="87,238,67,255"/>
                 <prop k="joinstyle" v="bevel"/>
                 <prop k="offset" v="0,0"/>
                 <prop k="offset_map_unit_scale" v="0.0001,0,0,0,0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="outline_color" v="87,238,67,255"/>
                 <prop k="outline_style" v="solid"/>
                 <prop k="outline_width" v="0.26"/>
                 <prop k="outline_width_unit" v="MM"/>
                 <prop k="style" v="dense5"/>
                </layer>
               </symbol>
               <symbol alpha="1" clip_to_extent="1" type="fill" name="6">
                <layer pass="0" class="SimpleFill" locked="0">
                 <prop k="border_width_map_unit_scale" v="0.0001,0,0,0,0,0"/>
                 <prop k="color" v="255,255,255,255"/>
                 <prop k="joinstyle" v="bevel"/>
                 <prop k="offset" v="0,0"/>
                 <prop k="offset_map_unit_scale" v="0.0001,0,0,0,0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="outline_color" v="0,0,0,255"/>
                 <prop k="outline_style" v="solid"/>
                 <prop k="outline_width" v="0.26"/>
                 <prop k="outline_width_unit" v="MM"/>
                 <prop k="style" v="solid"/>
                </layer>
               </symbol>
              </symbols>
              <source-symbol>
               <symbol alpha="1" clip_to_extent="1" type="fill" name="0">
                <layer pass="0" class="SimpleFill" locked="0">
                 <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
                 <prop k="color" v="100,167,71,255"/>
                 <prop k="joinstyle" v="bevel"/>
                 <prop k="offset" v="0,0"/>
                 <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="outline_color" v="0,0,0,255"/>
                 <prop k="outline_style" v="solid"/>
                 <prop k="outline_width" v="0.26"/>
                 <prop k="outline_width_unit" v="MM"/>
                 <prop k="style" v="solid"/>
                </layer>
               </symbol>
              </source-symbol>
              <rotation/>
              <sizescale scalemethod="diameter"/>
             </renderer-v2>
             <labeling type="simple"/>
             <customproperties>
              <property key="labeling" value="pal"/>
              <property key="labeling/addDirectionSymbol" value="false"/>
              <property key="labeling/angleOffset" value="0"/>
              <property key="labeling/blendMode" value="0"/>
              <property key="labeling/bufferBlendMode" value="0"/>
              <property key="labeling/bufferColorA" value="255"/>
              <property key="labeling/bufferColorB" value="255"/>
              <property key="labeling/bufferColorG" value="255"/>
              <property key="labeling/bufferColorR" value="255"/>
              <property key="labeling/bufferDraw" value="false"/>
              <property key="labeling/bufferJoinStyle" value="64"/>
              <property key="labeling/bufferNoFill" value="false"/>
              <property key="labeling/bufferSize" value="1"/>
              <property key="labeling/bufferSizeInMapUnits" value="false"/>
              <property key="labeling/bufferSizeMapUnitMaxScale" value="0"/>
              <property key="labeling/bufferSizeMapUnitMinScale" value="0"/>
              <property key="labeling/bufferTransp" value="0"/>
              <property key="labeling/centroidInside" value="false"/>
              <property key="labeling/centroidWhole" value="false"/>
              <property key="labeling/decimals" value="3"/>
              <property key="labeling/displayAll" value="false"/>
              <property key="labeling/dist" value="0"/>
              <property key="labeling/distInMapUnits" value="false"/>
              <property key="labeling/distMapUnitMaxScale" value="0"/>
              <property key="labeling/distMapUnitMinScale" value="0"/>
              <property key="labeling/drawLabels" value="false"/>
              <property key="labeling/enabled" value="false"/>
              <property key="labeling/fieldName" value=""/>
              <property key="labeling/fitInPolygonOnly" value="false"/>
              <property key="labeling/fontBold" value="false"/>
              <property key="labeling/fontCapitals" value="0"/>
              <property key="labeling/fontFamily" value="Noto Sans"/>
              <property key="labeling/fontItalic" value="false"/>
              <property key="labeling/fontLetterSpacing" value="0"/>
              <property key="labeling/fontLimitPixelSize" value="false"/>
              <property key="labeling/fontMaxPixelSize" value="10000"/>
              <property key="labeling/fontMinPixelSize" value="3"/>
              <property key="labeling/fontSize" value="9"/>
              <property key="labeling/fontSizeInMapUnits" value="false"/>
              <property key="labeling/fontSizeMapUnitMaxScale" value="0"/>
              <property key="labeling/fontSizeMapUnitMinScale" value="0"/>
              <property key="labeling/fontStrikeout" value="false"/>
              <property key="labeling/fontUnderline" value="false"/>
              <property key="labeling/fontWeight" value="50"/>
              <property key="labeling/fontWordSpacing" value="0"/>
              <property key="labeling/formatNumbers" value="false"/>
              <property key="labeling/isExpression" value="true"/>
              <property key="labeling/labelOffsetInMapUnits" value="true"/>
              <property key="labeling/labelOffsetMapUnitMaxScale" value="0"/>
              <property key="labeling/labelOffsetMapUnitMinScale" value="0"/>
              <property key="labeling/labelPerPart" value="false"/>
              <property key="labeling/leftDirectionSymbol" value="&lt;"/>
              <property key="labeling/limitNumLabels" value="false"/>
              <property key="labeling/maxCurvedCharAngleIn" value="20"/>
              <property key="labeling/maxCurvedCharAngleOut" value="-20"/>
              <property key="labeling/maxNumLabels" value="2000"/>
              <property key="labeling/mergeLines" value="false"/>
              <property key="labeling/minFeatureSize" value="0"/>
              <property key="labeling/multilineAlign" value="0"/>
              <property key="labeling/multilineHeight" value="1"/>
              <property key="labeling/namedStyle" value="Regular"/>
              <property key="labeling/obstacle" value="true"/>
              <property key="labeling/obstacleFactor" value="1"/>
              <property key="labeling/obstacleType" value="0"/>
              <property key="labeling/placeDirectionSymbol" value="0"/>
              <property key="labeling/placement" value="1"/>
              <property key="labeling/placementFlags" value="10"/>
              <property key="labeling/plussign" value="false"/>
              <property key="labeling/preserveRotation" value="true"/>
              <property key="labeling/previewBkgrdColor" value="#ffffff"/>
              <property key="labeling/priority" value="5"/>
              <property key="labeling/quadOffset" value="4"/>
              <property key="labeling/repeatDistance" value="0"/>
              <property key="labeling/repeatDistanceMapUnitMaxScale" value="0"/>
              <property key="labeling/repeatDistanceMapUnitMinScale" value="0"/>
              <property key="labeling/repeatDistanceUnit" value="1"/>
              <property key="labeling/reverseDirectionSymbol" value="false"/>
              <property key="labeling/rightDirectionSymbol" value=">"/>
              <property key="labeling/scaleMax" value="10000000"/>
              <property key="labeling/scaleMin" value="1"/>
              <property key="labeling/scaleVisibility" value="false"/>
              <property key="labeling/shadowBlendMode" value="6"/>
              <property key="labeling/shadowColorB" value="0"/>
              <property key="labeling/shadowColorG" value="0"/>
              <property key="labeling/shadowColorR" value="0"/>
              <property key="labeling/shadowDraw" value="false"/>
              <property key="labeling/shadowOffsetAngle" value="135"/>
              <property key="labeling/shadowOffsetDist" value="1"/>
              <property key="labeling/shadowOffsetGlobal" value="true"/>
              <property key="labeling/shadowOffsetMapUnitMaxScale" value="0"/>
              <property key="labeling/shadowOffsetMapUnitMinScale" value="0"/>
              <property key="labeling/shadowOffsetUnits" value="1"/>
              <property key="labeling/shadowRadius" value="1.5"/>
              <property key="labeling/shadowRadiusAlphaOnly" value="false"/>
              <property key="labeling/shadowRadiusMapUnitMaxScale" value="0"/>
              <property key="labeling/shadowRadiusMapUnitMinScale" value="0"/>
              <property key="labeling/shadowRadiusUnits" value="1"/>
              <property key="labeling/shadowScale" value="100"/>
              <property key="labeling/shadowTransparency" value="30"/>
              <property key="labeling/shadowUnder" value="0"/>
              <property key="labeling/shapeBlendMode" value="0"/>
              <property key="labeling/shapeBorderColorA" value="255"/>
              <property key="labeling/shapeBorderColorB" value="128"/>
              <property key="labeling/shapeBorderColorG" value="128"/>
              <property key="labeling/shapeBorderColorR" value="128"/>
              <property key="labeling/shapeBorderWidth" value="0"/>
              <property key="labeling/shapeBorderWidthMapUnitMaxScale" value="0"/>
              <property key="labeling/shapeBorderWidthMapUnitMinScale" value="0"/>
              <property key="labeling/shapeBorderWidthUnits" value="1"/>
              <property key="labeling/shapeDraw" value="false"/>
              <property key="labeling/shapeFillColorA" value="255"/>
              <property key="labeling/shapeFillColorB" value="255"/>
              <property key="labeling/shapeFillColorG" value="255"/>
              <property key="labeling/shapeFillColorR" value="255"/>
              <property key="labeling/shapeJoinStyle" value="64"/>
              <property key="labeling/shapeOffsetMapUnitMaxScale" value="0"/>
              <property key="labeling/shapeOffsetMapUnitMinScale" value="0"/>
              <property key="labeling/shapeOffsetUnits" value="1"/>
              <property key="labeling/shapeOffsetX" value="0"/>
              <property key="labeling/shapeOffsetY" value="0"/>
              <property key="labeling/shapeRadiiMapUnitMaxScale" value="0"/>
              <property key="labeling/shapeRadiiMapUnitMinScale" value="0"/>
              <property key="labeling/shapeRadiiUnits" value="1"/>
              <property key="labeling/shapeRadiiX" value="0"/>
              <property key="labeling/shapeRadiiY" value="0"/>
              <property key="labeling/shapeRotation" value="0"/>
              <property key="labeling/shapeRotationType" value="0"/>
              <property key="labeling/shapeSVGFile" value=""/>
              <property key="labeling/shapeSizeMapUnitMaxScale" value="0"/>
              <property key="labeling/shapeSizeMapUnitMinScale" value="0"/>
              <property key="labeling/shapeSizeType" value="0"/>
              <property key="labeling/shapeSizeUnits" value="1"/>
              <property key="labeling/shapeSizeX" value="0"/>
              <property key="labeling/shapeSizeY" value="0"/>
              <property key="labeling/shapeTransparency" value="0"/>
              <property key="labeling/shapeType" value="0"/>
              <property key="labeling/textColorA" value="255"/>
              <property key="labeling/textColorB" value="0"/>
              <property key="labeling/textColorG" value="0"/>
              <property key="labeling/textColorR" value="0"/>
              <property key="labeling/textTransp" value="0"/>
              <property key="labeling/upsidedownLabels" value="0"/>
              <property key="labeling/wrapChar" value=""/>
              <property key="labeling/xOffset" value="0"/>
              <property key="labeling/yOffset" value="0"/>
              <property key="variableNames" value="_fields_"/>
              <property key="variableValues" value=""/>
             </customproperties>
             <blendMode>0</blendMode>
             <featureBlendMode>0</featureBlendMode>
             <layerTransparency>0</layerTransparency>
             <displayfield>OBJECTID</displayfield>
             <label>0</label>
             <labelattributes>
              <label fieldname="" text="Label"/>
              <family fieldname="" name="MS Shell Dlg 2"/>
              <size fieldname="" units="pt" value="12"/>
              <bold fieldname="" on="0"/>
              <italic fieldname="" on="0"/>
              <underline fieldname="" on="0"/>
              <strikeout fieldname="" on="0"/>
              <color fieldname="" red="0" blue="0" green="0"/>
              <x fieldname=""/>
              <y fieldname=""/>
              <offset x="0" y="0" units="pt" yfieldname="" xfieldname=""/>
              <angle fieldname="" value="0" auto="0"/>
              <alignment fieldname="" value="center"/>
              <buffercolor fieldname="" red="255" blue="255" green="255"/>
              <buffersize fieldname="" units="pt" value="1"/>
              <bufferenabled fieldname="" on=""/>
              <multilineenabled fieldname="" on=""/>
              <selectedonly on=""/>
             </labelattributes>
             <SingleCategoryDiagramRenderer diagramType="Pie">
              <DiagramCategory penColor="#000000" labelPlacementMethod="XHeight" penWidth="0" diagramOrientation="Up" minimumSize="0" barWidth="5" penAlpha="255" maxScaleDenominator="1e+08" backgroundColor="#ffffff" transparency="0" width="15" scaleDependency="Area" backgroundAlpha="255" angleOffset="1440" scaleBasedVisibility="0" enabled="0" height="15" sizeType="MM" minScaleDenominator="-4.65661e-10">
               <fontProperties description="Noto Sans,9,-1,5,50,0,0,0,0,0" style=""/>
              </DiagramCategory>
             </SingleCategoryDiagramRenderer>
             <DiagramLayerSettings yPosColumn="-1" linePlacementFlags="10" placement="0" dist="0" xPosColumn="-1" priority="0" obstacle="0" showAll="1"/>
             <editform></editform>
             <editforminit/>
             <featformsuppress>0</featformsuppress>
             <annotationform></annotationform>
             <editorlayout>generatedlayout</editorlayout>
             <excludeAttributesWMS/>
             <excludeAttributesWFS/>
             <attributeactions/>
             <conditionalstyles>
              <rowstyles/>
              <fieldstyles/>
             </conditionalstyles>
            </qgis>
            ','<?xml version="1.0" encoding="UTF-8"?>
            <StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1.0" xmlns:xlink="http://www.w3.org/1999/xlink" units="mm" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" xmlns:se="http://www.opengis.net/se">
             <NamedLayer>
              <se:Name>rdpoly</se:Name>
              <UserStyle>
               <se:Name>rdpoly</se:Name>
               <se:FeatureTypeStyle>
                <se:Rule>
                 <se:Name>Unassigned</se:Name>
                 <se:Description>
                  <se:Title>Unassigned</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>1</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:PolygonSymbolizer>
                  <se:Fill>
                   <se:GraphicFill>
                    <se:Graphic>
                     <se:Mark>
                      <se:WellKnownName>brush://dense4</se:WellKnownName>
                      <se:Fill>
                       <se:SvgParameter name="fill">#ffaa00</se:SvgParameter>
                      </se:Fill>
                     </se:Mark>
                    </se:Graphic>
                   </se:GraphicFill>
                  </se:Fill>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#e48d3b</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                  </se:Stroke>
                 </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Multiple</se:Name>
                 <se:Description>
                  <se:Title>Multiple</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>2</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:PolygonSymbolizer>
                  <se:Fill>
                   <se:GraphicFill>
                    <se:Graphic>
                     <se:Mark>
                      <se:WellKnownName>brush://dense5</se:WellKnownName>
                      <se:Fill>
                       <se:SvgParameter name="fill">#ff0000</se:SvgParameter>
                      </se:Fill>
                     </se:Mark>
                    </se:Graphic>
                   </se:GraphicFill>
                  </se:Fill>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#e32a39</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                  </se:Stroke>
                 </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Public</se:Name>
                 <se:Description>
                  <se:Title>Public</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>11</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:PolygonSymbolizer>
                  <se:Fill>
                   <se:GraphicFill>
                    <se:Graphic>
                     <se:Mark>
                      <se:WellKnownName>brush://dense4</se:WellKnownName>
                      <se:Fill>
                       <se:SvgParameter name="fill">#157582</se:SvgParameter>
                      </se:Fill>
                     </se:Mark>
                    </se:Graphic>
                   </se:GraphicFill>
                  </se:Fill>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#157582</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                  </se:Stroke>
                 </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Prospective Public</se:Name>
                 <se:Description>
                  <se:Title>Prospective Public</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>12</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:PolygonSymbolizer>
                  <se:Fill>
                   <se:GraphicFill>
                    <se:Graphic>
                     <se:Mark>
                      <se:WellKnownName>brush://dense4</se:WellKnownName>
                      <se:Fill>
                       <se:SvgParameter name="fill">#00ffc5</se:SvgParameter>
                      </se:Fill>
                     </se:Mark>
                    </se:Graphic>
                   </se:GraphicFill>
                  </se:Fill>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#2af9d0</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                  </se:Stroke>
                 </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Private</se:Name>
                 <se:Description>
                  <se:Title>Private</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>13</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:PolygonSymbolizer>
                  <se:Fill>
                   <se:GraphicFill>
                    <se:Graphic>
                     <se:Mark>
                      <se:WellKnownName>brush://dense4</se:WellKnownName>
                      <se:Fill>
                       <se:SvgParameter name="fill">#38a800</se:SvgParameter>
                      </se:Fill>
                     </se:Mark>
                    </se:Graphic>
                   </se:GraphicFill>
                  </se:Fill>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#33a02c</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                  </se:Stroke>
                 </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Trunk</se:Name>
                 <se:Description>
                  <se:Title>Trunk</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>14</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:PolygonSymbolizer>
                  <se:Fill>
                   <se:GraphicFill>
                    <se:Graphic>
                     <se:Mark>
                      <se:WellKnownName>brush://dense5</se:WellKnownName>
                      <se:Fill>
                       <se:SvgParameter name="fill">#57ee43</se:SvgParameter>
                      </se:Fill>
                     </se:Mark>
                    </se:Graphic>
                   </se:GraphicFill>
                  </se:Fill>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#57ee43</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                  </se:Stroke>
                 </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Default</se:Name>
                 <se:Description>
                  <se:Title>Default</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal></ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:PolygonSymbolizer>
                  <se:Fill>
                   <se:SvgParameter name="fill">#ffffff</se:SvgParameter>
                  </se:Fill>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#000000</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                  </se:Stroke>
                 </se:PolygonSymbolizer>
                </se:Rule>
               </se:FeatureTypeStyle>
              </UserStyle>
             </NamedLayer>
            </StyledLayerDescriptor>
            ',1,'Fri Feb 12 14:53:15 2016',NULL,NULL,'2016-02-12 14:53:15');
INSERT INTO "layer_styles" VALUES(2,'roadnet_demo.sqlite','','esu','geometry','esu','<!DOCTYPE qgis PUBLIC ''http://mrcc.com/qgis.dtd'' ''SYSTEM''>
            <qgis version="2.8.6-Wien" minimumScale="-4.65661e-10" maximumScale="1e+08" simplifyDrawingHints="3" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="2.2" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0">
             <edittypes>
              <edittype widgetv2type="TextEdit" name="PK_UID">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="esu_id">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
              <edittype widgetv2type="TextEdit" name="symbol">
               <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
              </edittype>
             </edittypes>
             <renderer-v2 attr="SYMBOL" symbollevels="0" type="categorizedSymbol">
              <categories>
               <category render="true" symbol="0" value="0" label="Unassigned"/>
               <category render="true" symbol="1" value="1" label="Invalid"/>
               <category render="true" symbol="2" value="10" label="Type 1"/>
               <category render="true" symbol="3" value="11" label="Type 2"/>
               <category render="true" symbol="4" value="12" label="Type 1 + 3"/>
               <category render="true" symbol="5" value="13" label="Type 2 + 3"/>
               <category render="true" symbol="6" value="14" label="Type 1 + 4"/>
               <category render="true" symbol="7" value="15" label="Type 2 + 4"/>
               <category render="true" symbol="8" value="16" label="Type 1 + 3 + 4"/>
               <category render="true" symbol="9" value="17" label="Type 2 + 3 + 4"/>
               <category render="true" symbol="10" value="" label="Unsaved"/>
              </categories>
              <symbols>
               <symbol alpha="1" type="line" name="0">
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="178,178,178,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="0.3"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
               </symbol>
               <symbol alpha="1" type="line" name="1">
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="255,85,0,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="1"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
               </symbol>
               <symbol alpha="1" type="line" name="10">
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="square"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="bevel"/>
                 <prop k="line_color" v="132,35,72,255"/>
                 <prop k="line_style" v="dash"/>
                 <prop k="line_width" v="0.26"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
               </symbol>
               <symbol alpha="1" type="line" name="2">
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="56,168,0,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="1"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
               </symbol>
               <symbol alpha="1" type="line" name="3">
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="0,77,168,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="1"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
               </symbol>
               <symbol alpha="1" type="line" name="4">
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="0,0,0,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="2"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="76,230,0,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="1"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
               </symbol>
               <symbol alpha="1" type="line" name="5">
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="0,0,0,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="2"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="0,197,255,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="1"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
               </symbol>
               <symbol alpha="1" type="line" name="6">
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="230,0,0,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="2"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="85,255,0,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="1"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
               </symbol>
               <symbol alpha="1" type="line" name="7">
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="230,0,0,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="2"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="0,197,255,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="1"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
               </symbol>
               <symbol alpha="1" type="line" name="8">
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="230,0,0,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="4"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="0,0,0,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="2"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="85,255,0,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="1"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
               </symbol>
               <symbol alpha="1" type="line" name="9">
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="230,0,0,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="4"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="0,0,0,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="2"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="flat"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="round"/>
                 <prop k="line_color" v="0,197,255,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="1"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
               </symbol>
              </symbols>
              <source-symbol>
               <symbol alpha="1" type="line" name="0">
                <layer pass="0" class="SimpleLine" locked="0">
                 <prop k="capstyle" v="square"/>
                 <prop k="customdash" v="5;2"/>
                 <prop k="customdash_map_unit_scale" v="0,0"/>
                 <prop k="customdash_unit" v="MM"/>
                 <prop k="draw_inside_polygon" v="0"/>
                 <prop k="joinstyle" v="bevel"/>
                 <prop k="line_color" v="106,98,152,255"/>
                 <prop k="line_style" v="solid"/>
                 <prop k="line_width" v="0.26"/>
                 <prop k="line_width_unit" v="MM"/>
                 <prop k="offset" v="0"/>
                 <prop k="offset_map_unit_scale" v="0,0"/>
                 <prop k="offset_unit" v="MM"/>
                 <prop k="use_custom_dash" v="0"/>
                 <prop k="width_map_unit_scale" v="0,0"/>
                </layer>
               </symbol>
              </source-symbol>
              <rotation/>
              <sizescale scalemethod="diameter"/>
             </renderer-v2>
             <customproperties>
              <property key="labeling" value="pal"/>
              <property key="labeling/addDirectionSymbol" value="false"/>
              <property key="labeling/angleOffset" value="0"/>
              <property key="labeling/blendMode" value="0"/>
              <property key="labeling/bufferBlendMode" value="0"/>
              <property key="labeling/bufferColorA" value="255"/>
              <property key="labeling/bufferColorB" value="255"/>
              <property key="labeling/bufferColorG" value="255"/>
              <property key="labeling/bufferColorR" value="255"/>
              <property key="labeling/bufferDraw" value="false"/>
              <property key="labeling/bufferJoinStyle" value="64"/>
              <property key="labeling/bufferNoFill" value="false"/>
              <property key="labeling/bufferSize" value="1"/>
              <property key="labeling/bufferSizeInMapUnits" value="false"/>
              <property key="labeling/bufferSizeMapUnitMaxScale" value="0"/>
              <property key="labeling/bufferSizeMapUnitMinScale" value="0"/>
              <property key="labeling/bufferTransp" value="0"/>
              <property key="labeling/centroidInside" value="false"/>
              <property key="labeling/centroidWhole" value="false"/>
              <property key="labeling/decimals" value="3"/>
              <property key="labeling/displayAll" value="false"/>
              <property key="labeling/dist" value="0"/>
              <property key="labeling/distInMapUnits" value="false"/>
              <property key="labeling/distMapUnitMaxScale" value="0"/>
              <property key="labeling/distMapUnitMinScale" value="0"/>
              <property key="labeling/drawLabels" value="false"/>
              <property key="labeling/enabled" value="false"/>
              <property key="labeling/fieldName" value=""/>
              <property key="labeling/fitInPolygonOnly" value="false"/>
              <property key="labeling/fontBold" value="false"/>
              <property key="labeling/fontCapitals" value="0"/>
              <property key="labeling/fontFamily" value="MS Shell Dlg 2"/>
              <property key="labeling/fontItalic" value="false"/>
              <property key="labeling/fontLetterSpacing" value="0"/>
              <property key="labeling/fontLimitPixelSize" value="false"/>
              <property key="labeling/fontMaxPixelSize" value="10000"/>
              <property key="labeling/fontMinPixelSize" value="3"/>
              <property key="labeling/fontSize" value="9"/>
              <property key="labeling/fontSizeInMapUnits" value="false"/>
              <property key="labeling/fontSizeMapUnitMaxScale" value="0"/>
              <property key="labeling/fontSizeMapUnitMinScale" value="0"/>
              <property key="labeling/fontStrikeout" value="false"/>
              <property key="labeling/fontUnderline" value="false"/>
              <property key="labeling/fontWeight" value="50"/>
              <property key="labeling/fontWordSpacing" value="0"/>
              <property key="labeling/formatNumbers" value="false"/>
              <property key="labeling/isExpression" value="true"/>
              <property key="labeling/labelOffsetInMapUnits" value="true"/>
              <property key="labeling/labelOffsetMapUnitMaxScale" value="0"/>
              <property key="labeling/labelOffsetMapUnitMinScale" value="0"/>
              <property key="labeling/labelPerPart" value="false"/>
              <property key="labeling/leftDirectionSymbol" value="&lt;"/>
              <property key="labeling/limitNumLabels" value="false"/>
              <property key="labeling/maxCurvedCharAngleIn" value="20"/>
              <property key="labeling/maxCurvedCharAngleOut" value="-20"/>
              <property key="labeling/maxNumLabels" value="2000"/>
              <property key="labeling/mergeLines" value="false"/>
              <property key="labeling/minFeatureSize" value="0"/>
              <property key="labeling/multilineAlign" value="0"/>
              <property key="labeling/multilineHeight" value="1"/>
              <property key="labeling/namedStyle" value="Normal"/>
              <property key="labeling/obstacle" value="true"/>
              <property key="labeling/obstacleFactor" value="1"/>
              <property key="labeling/obstacleType" value="0"/>
              <property key="labeling/placeDirectionSymbol" value="0"/>
              <property key="labeling/placement" value="2"/>
              <property key="labeling/placementFlags" value="10"/>
              <property key="labeling/plussign" value="false"/>
              <property key="labeling/preserveRotation" value="true"/>
              <property key="labeling/previewBkgrdColor" value="#ffffff"/>
              <property key="labeling/priority" value="5"/>
              <property key="labeling/quadOffset" value="4"/>
              <property key="labeling/repeatDistance" value="0"/>
              <property key="labeling/repeatDistanceMapUnitMaxScale" value="0"/>
              <property key="labeling/repeatDistanceMapUnitMinScale" value="0"/>
              <property key="labeling/repeatDistanceUnit" value="1"/>
              <property key="labeling/reverseDirectionSymbol" value="false"/>
              <property key="labeling/rightDirectionSymbol" value=">"/>
              <property key="labeling/scaleMax" value="10000000"/>
              <property key="labeling/scaleMin" value="1"/>
              <property key="labeling/scaleVisibility" value="false"/>
              <property key="labeling/shadowBlendMode" value="6"/>
              <property key="labeling/shadowColorB" value="0"/>
              <property key="labeling/shadowColorG" value="0"/>
              <property key="labeling/shadowColorR" value="0"/>
              <property key="labeling/shadowDraw" value="false"/>
              <property key="labeling/shadowOffsetAngle" value="135"/>
              <property key="labeling/shadowOffsetDist" value="1"/>
              <property key="labeling/shadowOffsetGlobal" value="true"/>
              <property key="labeling/shadowOffsetMapUnitMaxScale" value="0"/>
              <property key="labeling/shadowOffsetMapUnitMinScale" value="0"/>
              <property key="labeling/shadowOffsetUnits" value="1"/>
              <property key="labeling/shadowRadius" value="1.5"/>
              <property key="labeling/shadowRadiusAlphaOnly" value="false"/>
              <property key="labeling/shadowRadiusMapUnitMaxScale" value="0"/>
              <property key="labeling/shadowRadiusMapUnitMinScale" value="0"/>
              <property key="labeling/shadowRadiusUnits" value="1"/>
              <property key="labeling/shadowScale" value="100"/>
              <property key="labeling/shadowTransparency" value="30"/>
              <property key="labeling/shadowUnder" value="0"/>
              <property key="labeling/shapeBlendMode" value="0"/>
              <property key="labeling/shapeBorderColorA" value="255"/>
              <property key="labeling/shapeBorderColorB" value="128"/>
              <property key="labeling/shapeBorderColorG" value="128"/>
              <property key="labeling/shapeBorderColorR" value="128"/>
              <property key="labeling/shapeBorderWidth" value="0"/>
              <property key="labeling/shapeBorderWidthMapUnitMaxScale" value="0"/>
              <property key="labeling/shapeBorderWidthMapUnitMinScale" value="0"/>
              <property key="labeling/shapeBorderWidthUnits" value="1"/>
              <property key="labeling/shapeDraw" value="false"/>
              <property key="labeling/shapeFillColorA" value="255"/>
              <property key="labeling/shapeFillColorB" value="255"/>
              <property key="labeling/shapeFillColorG" value="255"/>
              <property key="labeling/shapeFillColorR" value="255"/>
              <property key="labeling/shapeJoinStyle" value="64"/>
              <property key="labeling/shapeOffsetMapUnitMaxScale" value="0"/>
              <property key="labeling/shapeOffsetMapUnitMinScale" value="0"/>
              <property key="labeling/shapeOffsetUnits" value="1"/>
              <property key="labeling/shapeOffsetX" value="0"/>
              <property key="labeling/shapeOffsetY" value="0"/>
              <property key="labeling/shapeRadiiMapUnitMaxScale" value="0"/>
              <property key="labeling/shapeRadiiMapUnitMinScale" value="0"/>
              <property key="labeling/shapeRadiiUnits" value="1"/>
              <property key="labeling/shapeRadiiX" value="0"/>
              <property key="labeling/shapeRadiiY" value="0"/>
              <property key="labeling/shapeRotation" value="0"/>
              <property key="labeling/shapeRotationType" value="0"/>
              <property key="labeling/shapeSVGFile" value=""/>
              <property key="labeling/shapeSizeMapUnitMaxScale" value="0"/>
              <property key="labeling/shapeSizeMapUnitMinScale" value="0"/>
              <property key="labeling/shapeSizeType" value="0"/>
              <property key="labeling/shapeSizeUnits" value="1"/>
              <property key="labeling/shapeSizeX" value="0"/>
              <property key="labeling/shapeSizeY" value="0"/>
              <property key="labeling/shapeTransparency" value="0"/>
              <property key="labeling/shapeType" value="0"/>
              <property key="labeling/textColorA" value="255"/>
              <property key="labeling/textColorB" value="0"/>
              <property key="labeling/textColorG" value="0"/>
              <property key="labeling/textColorR" value="0"/>
              <property key="labeling/textTransp" value="0"/>
              <property key="labeling/upsidedownLabels" value="0"/>
              <property key="labeling/wrapChar" value=""/>
              <property key="labeling/xOffset" value="0"/>
              <property key="labeling/yOffset" value="0"/>
             </customproperties>
             <blendMode>0</blendMode>
             <featureBlendMode>0</featureBlendMode>
             <layerTransparency>0</layerTransparency>
             <displayfield>OBJECTID</displayfield>
             <label>0</label>
             <labelattributes>
              <label fieldname="" text="Label"/>
              <family fieldname="" name="MS Shell Dlg 2"/>
              <size fieldname="" units="pt" value="12"/>
              <bold fieldname="" on="0"/>
              <italic fieldname="" on="0"/>
              <underline fieldname="" on="0"/>
              <strikeout fieldname="" on="0"/>
              <color fieldname="" red="0" blue="0" green="0"/>
              <x fieldname=""/>
              <y fieldname=""/>
              <offset x="0" y="0" units="pt" yfieldname="" xfieldname=""/>
              <angle fieldname="" value="0" auto="0"/>
              <alignment fieldname="" value="center"/>
              <buffercolor fieldname="" red="255" blue="255" green="255"/>
              <buffersize fieldname="" units="pt" value="1"/>
              <bufferenabled fieldname="" on=""/>
              <multilineenabled fieldname="" on=""/>
              <selectedonly on=""/>
             </labelattributes>
             <editform></editform>
             <editforminit/>
             <featformsuppress>0</featformsuppress>
             <annotationform></annotationform>
             <editorlayout>generatedlayout</editorlayout>
             <excludeAttributesWMS/>
             <excludeAttributesWFS/>
             <attributeactions/>
            </qgis>
            ','<?xml version="1.0" encoding="UTF-8"?>
            <StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1.0" xmlns:xlink="http://www.w3.org/1999/xlink" units="mm" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" xmlns:se="http://www.opengis.net/se">
             <NamedLayer>
              <se:Name>ESU Graphic</se:Name>
              <UserStyle>
               <se:Name>ESU Graphic</se:Name>
               <se:FeatureTypeStyle>
                <se:Rule>
                 <se:Name>Unassigned</se:Name>
                 <se:Description>
                  <se:Title>Unassigned</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>0</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#b2b2b2</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">0.3</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Invalid</se:Name>
                 <se:Description>
                  <se:Title>Invalid</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>1</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#ff5500</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Type 1</se:Name>
                 <se:Description>
                  <se:Title>Type 1</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>10</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#38a800</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Type 2</se:Name>
                 <se:Description>
                  <se:Title>Type 2</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>11</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#004da8</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Type 1 + 3</se:Name>
                 <se:Description>
                  <se:Title>Type 1 + 3</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>12</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#000000</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">2</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#4ce600</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Type 2 + 3</se:Name>
                 <se:Description>
                  <se:Title>Type 2 + 3</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>13</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#000000</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">2</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#00c5ff</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Type 1 + 4</se:Name>
                 <se:Description>
                  <se:Title>Type 1 + 4</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>14</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#e60000</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">2</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#55ff00</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Type 2 + 4</se:Name>
                 <se:Description>
                  <se:Title>Type 2 + 4</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>15</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#e60000</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">2</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#00c5ff</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Type 1 + 3 + 4</se:Name>
                 <se:Description>
                  <se:Title>Type 1 + 3 + 4</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>16</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#e60000</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">4</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#000000</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">2</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#55ff00</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Type 2 + 3 + 4</se:Name>
                 <se:Description>
                  <se:Title>Type 2 + 3 + 4</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal>17</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#e60000</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">4</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#000000</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">2</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#00c5ff</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">butt</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                 <se:Name>Unsaved</se:Name>
                 <se:Description>
                  <se:Title>Unsaved</se:Title>
                 </se:Description>
                 <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                  <ogc:PropertyIsEqualTo>
                   <ogc:PropertyName>SYMBOL</ogc:PropertyName>
                   <ogc:Literal></ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                 </ogc:Filter>
                 <se:LineSymbolizer>
                  <se:Stroke>
                   <se:SvgParameter name="stroke">#842348</se:SvgParameter>
                   <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
                   <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                   <se:SvgParameter name="stroke-linecap">square</se:SvgParameter>
                   <se:SvgParameter name="stroke-dasharray">4 2</se:SvgParameter>
                  </se:Stroke>
                 </se:LineSymbolizer>
                </se:Rule>
               </se:FeatureTypeStyle>
              </UserStyle>
             </NamedLayer>
            </StyledLayerDescriptor>
            ',1,'Mon 15. Feb 11:17:04 2016',NULL,NULL,'2016-02-15 11:09:03');
INSERT INTO "layer_styles" VALUES(10,'roadnet_demo.sqlite','','mcl','geometry','mcl','<!DOCTYPE qgis PUBLIC ''http://mrcc.com/qgis.dtd'' ''SYSTEM''>
<qgis version="2.12.0-Lyon" minimumScale="0" maximumScale="1e+08" simplifyDrawingHints="1" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0">
 <edittypes>
  <edittype widgetv2type="TextEdit" name="PK_UID">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="esu_id">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="symbol">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="usrn">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="rec_type">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="desc_text">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="locality">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="town">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="entry_date">
   <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="typ_3_usrn">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="typ_3_desc">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="typ_4_usrn">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="typ_4_desc">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="lor_ref_1">
   <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="lor_ref_2">
   <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="lor_desc">
   <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="lane_number">
   <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="speed_limit">
   <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="rural_urban_id">
   <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="section_type">
   <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="adoption_status">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="mcl_ref">
   <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="street_classification">
   <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="in_pilot">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="carriageway">
   <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/>
  </edittype>
 </edittypes>
 <renderer-v2 attr="carriageway" forceraster="0" symbollevels="0" type="categorizedSymbol">
  <categories>
   <category render="true" symbol="0" value="" label="&lt;unassigned>"/>
   <category render="true" symbol="1" value="Dual" label="Dual"/>
   <category render="true" symbol="2" value="Single" label="Single"/>
  </categories>
  <symbols>
   <symbol alpha="1" clip_to_extent="1" type="line" name="0">
    <layer pass="0" class="SimpleLine" locked="0">
     <prop k="capstyle" v="square"/>
     <prop k="customdash" v="5;2"/>
     <prop k="customdash_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="customdash_unit" v="MM"/>
     <prop k="draw_inside_polygon" v="0"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="line_color" v="130,216,151,255"/>
     <prop k="line_style" v="solid"/>
     <prop k="line_width" v="0.46"/>
     <prop k="line_width_unit" v="MM"/>
     <prop k="offset" v="0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="use_custom_dash" v="0"/>
     <prop k="width_map_unit_scale" v="0,0,0,0,0,0"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="line" name="1">
    <layer pass="0" class="SimpleLine" locked="0">
     <prop k="capstyle" v="square"/>
     <prop k="customdash" v="5;2"/>
     <prop k="customdash_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="customdash_unit" v="MM"/>
     <prop k="draw_inside_polygon" v="0"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="line_color" v="13,7,166,255"/>
     <prop k="line_style" v="solid"/>
     <prop k="line_width" v="0.86"/>
     <prop k="line_width_unit" v="MM"/>
     <prop k="offset" v="0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="use_custom_dash" v="0"/>
     <prop k="width_map_unit_scale" v="0,0,0,0,0,0"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="line" name="2">
    <layer pass="0" class="SimpleLine" locked="0">
     <prop k="capstyle" v="square"/>
     <prop k="customdash" v="5;2"/>
     <prop k="customdash_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="customdash_unit" v="MM"/>
     <prop k="draw_inside_polygon" v="0"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="line_color" v="250,52,17,255"/>
     <prop k="line_style" v="solid"/>
     <prop k="line_width" v="0.66"/>
     <prop k="line_width_unit" v="MM"/>
     <prop k="offset" v="0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="use_custom_dash" v="0"/>
     <prop k="width_map_unit_scale" v="0,0,0,0,0,0"/>
    </layer>
   </symbol>
  </symbols>
  <source-symbol>
   <symbol alpha="1" clip_to_extent="1" type="line" name="0">
    <layer pass="0" class="SimpleLine" locked="0">
     <prop k="capstyle" v="square"/>
     <prop k="customdash" v="5;2"/>
     <prop k="customdash_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="customdash_unit" v="MM"/>
     <prop k="draw_inside_polygon" v="0"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="line_color" v="182,223,86,255"/>
     <prop k="line_style" v="solid"/>
     <prop k="line_width" v="0.26"/>
     <prop k="line_width_unit" v="MM"/>
     <prop k="offset" v="0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="use_custom_dash" v="0"/>
     <prop k="width_map_unit_scale" v="0,0,0,0,0,0"/>
    </layer>
   </symbol>
  </source-symbol>
  <rotation/>
  <sizescale scalemethod="diameter"/>
 </renderer-v2>
 <labeling type="rule-based">
  <rules>
   <rule scalemaxdenom="5000" description="MCL - all records" scalemindenom="10">
    <settings>
     <text-style fontItalic="0" fontFamily="Noto Sans" fontLetterSpacing="0" fontUnderline="0" fontSizeMapUnitMaxScale="0" fontWeight="50" fontStrikeout="0" textTransp="0" previewBkgrdColor="#ffffff" fontCapitals="0" textColor="250,52,17,255" fontSizeMapUnitMinScale="0" fontSizeInMapUnits="0" isExpression="1" blendMode="0" fontSize="11" fieldName="concat(&quot;lor_ref_1&quot;, ''/'',  &quot;lor_ref_2&quot;)" namedStyle="Regular" fontWordSpacing="0"/>
     <text-format placeDirectionSymbol="0" multilineAlign="0" rightDirectionSymbol=">" multilineHeight="1" plussign="0" addDirectionSymbol="0" leftDirectionSymbol="&lt;" formatNumbers="0" decimals="3" wrapChar="" reverseDirectionSymbol="0"/>
     <text-buffer bufferSize="1.8" bufferSizeMapUnitMinScale="0" bufferColor="255,255,255,255" bufferDraw="1" bufferBlendMode="0" bufferTransp="14" bufferSizeInMapUnits="0" bufferSizeMapUnitMaxScale="0" bufferNoFill="0" bufferJoinStyle="64"/>
     <background shapeSizeUnits="1" shapeType="0" shapeOffsetMapUnitMinScale="0" shapeSizeMapUnitMinScale="0" shapeSVGFile="" shapeOffsetX="0" shapeOffsetY="0" shapeBlendMode="0" shapeBorderWidthMapUnitMaxScale="0" shapeFillColor="255,255,255,255" shapeTransparency="0" shapeSizeType="0" shapeJoinStyle="64" shapeDraw="0" shapeSizeMapUnitMaxScale="0" shapeBorderWidthUnits="1" shapeSizeX="0" shapeSizeY="0" shapeRadiiX="0" shapeOffsetMapUnitMaxScale="0" shapeOffsetUnits="1" shapeRadiiY="0" shapeRotation="0" shapeBorderWidth="0" shapeRadiiMapUnitMinScale="0" shapeRadiiMapUnitMaxScale="0" shapeBorderColor="128,128,128,255" shapeRotationType="0" shapeRadiiUnits="1" shapeBorderWidthMapUnitMinScale="0"/>
     <shadow shadowOffsetGlobal="1" shadowRadiusUnits="1" shadowRadiusMapUnitMinScale="0" shadowTransparency="30" shadowColor="0,0,0,255" shadowUnder="0" shadowScale="100" shadowOffsetDist="1" shadowOffsetMapUnitMinScale="0" shadowRadiusMapUnitMaxScale="0" shadowDraw="0" shadowOffsetAngle="135" shadowRadius="1.5" shadowBlendMode="6" shadowOffsetMapUnitMaxScale="0" shadowRadiusAlphaOnly="0" shadowOffsetUnits="1"/>
     <placement repeatDistanceUnit="1" placement="2" maxCurvedCharAngleIn="20" repeatDistance="0" distMapUnitMaxScale="0" labelOffsetMapUnitMaxScale="0" distInMapUnits="0" labelOffsetInMapUnits="1" xOffset="0" preserveRotation="1" centroidWhole="0" priority="5" repeatDistanceMapUnitMaxScale="0" yOffset="0" placementFlags="10" repeatDistanceMapUnitMinScale="0" centroidInside="0" dist="0" angleOffset="0" maxCurvedCharAngleOut="-20" fitInPolygonOnly="0" quadOffset="4" distMapUnitMinScale="0" labelOffsetMapUnitMinScale="0"/>
     <rendering fontMinPixelSize="3" scaleMax="10000000" fontMaxPixelSize="10000" scaleMin="1" upsidedownLabels="0" limitNumLabels="0" obstacle="1" obstacleFactor="1" scaleVisibility="0" fontLimitPixelSize="0" mergeLines="0" obstacleType="0" labelPerPart="0" maxNumLabels="2000" displayAll="0" minFeatureSize="0"/>
     <data-defined/>
    </settings>
   </rule>
  </rules>
 </labeling>
 <customproperties>
  <property key="labeling/addDirectionSymbol" value="false"/>
  <property key="labeling/angleOffset" value="0"/>
  <property key="labeling/blendMode" value="0"/>
  <property key="labeling/bufferBlendMode" value="0"/>
  <property key="labeling/bufferColorA" value="255"/>
  <property key="labeling/bufferColorB" value="255"/>
  <property key="labeling/bufferColorG" value="255"/>
  <property key="labeling/bufferColorR" value="255"/>
  <property key="labeling/bufferDraw" value="true"/>
  <property key="labeling/bufferJoinStyle" value="64"/>
  <property key="labeling/bufferNoFill" value="false"/>
  <property key="labeling/bufferSize" value="1"/>
  <property key="labeling/bufferSizeInMapUnits" value="false"/>
  <property key="labeling/bufferSizeMapUnitMaxScale" value="0"/>
  <property key="labeling/bufferSizeMapUnitMinScale" value="0"/>
  <property key="labeling/bufferTransp" value="20"/>
  <property key="labeling/centroidInside" value="false"/>
  <property key="labeling/centroidWhole" value="false"/>
  <property key="labeling/decimals" value="3"/>
  <property key="labeling/displayAll" value="false"/>
  <property key="labeling/dist" value="0"/>
  <property key="labeling/distInMapUnits" value="false"/>
  <property key="labeling/distMapUnitMaxScale" value="0"/>
  <property key="labeling/distMapUnitMinScale" value="0"/>
  <property key="labeling/drawLabels" value="true"/>
  <property key="labeling/enabled" value="true"/>
  <property key="labeling/fieldName" value=" concat(&quot;lor_ref_1&quot;, ''/'', &quot;lor_ref_2&quot; )"/>
  <property key="labeling/fitInPolygonOnly" value="false"/>
  <property key="labeling/fontCapitals" value="0"/>
  <property key="labeling/fontFamily" value="Noto Sans"/>
  <property key="labeling/fontItalic" value="false"/>
  <property key="labeling/fontLetterSpacing" value="0"/>
  <property key="labeling/fontLimitPixelSize" value="false"/>
  <property key="labeling/fontMaxPixelSize" value="10000"/>
  <property key="labeling/fontMinPixelSize" value="3"/>
  <property key="labeling/fontSize" value="9"/>
  <property key="labeling/fontSizeInMapUnits" value="false"/>
  <property key="labeling/fontSizeMapUnitMaxScale" value="0"/>
  <property key="labeling/fontSizeMapUnitMinScale" value="0"/>
  <property key="labeling/fontStrikeout" value="false"/>
  <property key="labeling/fontUnderline" value="false"/>
  <property key="labeling/fontWeight" value="50"/>
  <property key="labeling/fontWordSpacing" value="0"/>
  <property key="labeling/formatNumbers" value="false"/>
  <property key="labeling/isExpression" value="true"/>
  <property key="labeling/labelOffsetInMapUnits" value="true"/>
  <property key="labeling/labelOffsetMapUnitMaxScale" value="0"/>
  <property key="labeling/labelOffsetMapUnitMinScale" value="0"/>
  <property key="labeling/labelPerPart" value="false"/>
  <property key="labeling/leftDirectionSymbol" value="&lt;"/>
  <property key="labeling/limitNumLabels" value="false"/>
  <property key="labeling/maxCurvedCharAngleIn" value="20"/>
  <property key="labeling/maxCurvedCharAngleOut" value="-20"/>
  <property key="labeling/maxNumLabels" value="2000"/>
  <property key="labeling/mergeLines" value="false"/>
  <property key="labeling/minFeatureSize" value="0"/>
  <property key="labeling/multilineAlign" value="0"/>
  <property key="labeling/multilineHeight" value="1"/>
  <property key="labeling/namedStyle" value="Regular"/>
  <property key="labeling/obstacle" value="true"/>
  <property key="labeling/obstacleFactor" value="1"/>
  <property key="labeling/obstacleType" value="0"/>
  <property key="labeling/placeDirectionSymbol" value="0"/>
  <property key="labeling/placement" value="2"/>
  <property key="labeling/placementFlags" value="10"/>
  <property key="labeling/plussign" value="false"/>
  <property key="labeling/preserveRotation" value="true"/>
  <property key="labeling/previewBkgrdColor" value="#ffffff"/>
  <property key="labeling/priority" value="5"/>
  <property key="labeling/quadOffset" value="4"/>
  <property key="labeling/repeatDistance" value="0"/>
  <property key="labeling/repeatDistanceMapUnitMaxScale" value="0"/>
  <property key="labeling/repeatDistanceMapUnitMinScale" value="0"/>
  <property key="labeling/repeatDistanceUnit" value="1"/>
  <property key="labeling/reverseDirectionSymbol" value="false"/>
  <property key="labeling/rightDirectionSymbol" value=">"/>
  <property key="labeling/scaleMax" value="10000000"/>
  <property key="labeling/scaleMin" value="1"/>
  <property key="labeling/scaleVisibility" value="false"/>
  <property key="labeling/shadowBlendMode" value="6"/>
  <property key="labeling/shadowColorB" value="0"/>
  <property key="labeling/shadowColorG" value="0"/>
  <property key="labeling/shadowColorR" value="0"/>
  <property key="labeling/shadowDraw" value="false"/>
  <property key="labeling/shadowOffsetAngle" value="135"/>
  <property key="labeling/shadowOffsetDist" value="1"/>
  <property key="labeling/shadowOffsetGlobal" value="true"/>
  <property key="labeling/shadowOffsetMapUnitMaxScale" value="0"/>
  <property key="labeling/shadowOffsetMapUnitMinScale" value="0"/>
  <property key="labeling/shadowOffsetUnits" value="1"/>
  <property key="labeling/shadowRadius" value="1.5"/>
  <property key="labeling/shadowRadiusAlphaOnly" value="false"/>
  <property key="labeling/shadowRadiusMapUnitMaxScale" value="0"/>
  <property key="labeling/shadowRadiusMapUnitMinScale" value="0"/>
  <property key="labeling/shadowRadiusUnits" value="1"/>
  <property key="labeling/shadowScale" value="100"/>
  <property key="labeling/shadowTransparency" value="30"/>
  <property key="labeling/shadowUnder" value="0"/>
  <property key="labeling/shapeBlendMode" value="0"/>
  <property key="labeling/shapeBorderColorA" value="255"/>
  <property key="labeling/shapeBorderColorB" value="128"/>
  <property key="labeling/shapeBorderColorG" value="128"/>
  <property key="labeling/shapeBorderColorR" value="128"/>
  <property key="labeling/shapeBorderWidth" value="0"/>
  <property key="labeling/shapeBorderWidthMapUnitMaxScale" value="0"/>
  <property key="labeling/shapeBorderWidthMapUnitMinScale" value="0"/>
  <property key="labeling/shapeBorderWidthUnits" value="1"/>
  <property key="labeling/shapeDraw" value="false"/>
  <property key="labeling/shapeFillColorA" value="255"/>
  <property key="labeling/shapeFillColorB" value="255"/>
  <property key="labeling/shapeFillColorG" value="255"/>
  <property key="labeling/shapeFillColorR" value="255"/>
  <property key="labeling/shapeJoinStyle" value="64"/>
  <property key="labeling/shapeOffsetMapUnitMaxScale" value="0"/>
  <property key="labeling/shapeOffsetMapUnitMinScale" value="0"/>
  <property key="labeling/shapeOffsetUnits" value="1"/>
  <property key="labeling/shapeOffsetX" value="0"/>
  <property key="labeling/shapeOffsetY" value="0"/>
  <property key="labeling/shapeRadiiMapUnitMaxScale" value="0"/>
  <property key="labeling/shapeRadiiMapUnitMinScale" value="0"/>
  <property key="labeling/shapeRadiiUnits" value="1"/>
  <property key="labeling/shapeRadiiX" value="0"/>
  <property key="labeling/shapeRadiiY" value="0"/>
  <property key="labeling/shapeRotation" value="0"/>
  <property key="labeling/shapeRotationType" value="0"/>
  <property key="labeling/shapeSVGFile" value=""/>
  <property key="labeling/shapeSizeMapUnitMaxScale" value="0"/>
  <property key="labeling/shapeSizeMapUnitMinScale" value="0"/>
  <property key="labeling/shapeSizeType" value="0"/>
  <property key="labeling/shapeSizeUnits" value="1"/>
  <property key="labeling/shapeSizeX" value="0"/>
  <property key="labeling/shapeSizeY" value="0"/>
  <property key="labeling/shapeTransparency" value="0"/>
  <property key="labeling/shapeType" value="0"/>
  <property key="labeling/textColorA" value="255"/>
  <property key="labeling/textColorB" value="17"/>
  <property key="labeling/textColorG" value="52"/>
  <property key="labeling/textColorR" value="250"/>
  <property key="labeling/textTransp" value="0"/>
  <property key="labeling/upsidedownLabels" value="0"/>
  <property key="labeling/wrapChar" value=""/>
  <property key="labeling/xOffset" value="0"/>
  <property key="labeling/yOffset" value="0"/>
  <property key="variableNames" value="_fields_"/>
  <property key="variableValues" value=""/>
 </customproperties>
 <blendMode>0</blendMode>
 <featureBlendMode>0</featureBlendMode>
 <layerTransparency>0</layerTransparency>
 <displayfield>PK_UID</displayfield>
 <label>0</label>
 <labelattributes>
  <label fieldname="" text="Label"/>
  <family fieldname="" name="Noto Sans"/>
  <size fieldname="" units="pt" value="12"/>
  <bold fieldname="" on="0"/>
  <italic fieldname="" on="0"/>
  <underline fieldname="" on="0"/>
  <strikeout fieldname="" on="0"/>
  <color fieldname="" red="0" blue="0" green="0"/>
  <x fieldname=""/>
  <y fieldname=""/>
  <offset x="0" y="0" units="pt" yfieldname="" xfieldname=""/>
  <angle fieldname="" value="0" auto="0"/>
  <alignment fieldname="" value="center"/>
  <buffercolor fieldname="" red="255" blue="255" green="255"/>
  <buffersize fieldname="" units="pt" value="1"/>
  <bufferenabled fieldname="" on=""/>
  <multilineenabled fieldname="" on=""/>
  <selectedonly on=""/>
 </labelattributes>
 <SingleCategoryDiagramRenderer diagramType="Pie">
  <DiagramCategory penColor="#000000" labelPlacementMethod="XHeight" penWidth="0" diagramOrientation="Up" minimumSize="0" barWidth="5" penAlpha="255" maxScaleDenominator="1e+08" backgroundColor="#ffffff" transparency="0" width="15" scaleDependency="Area" backgroundAlpha="255" angleOffset="1440" scaleBasedVisibility="0" enabled="0" height="15" sizeType="MM" minScaleDenominator="-4.65661e-10">
   <fontProperties description="Noto Sans,9,-1,5,50,0,0,0,0,0" style=""/>
   <attribute field="" color="#000000" label=""/>
  </DiagramCategory>
 </SingleCategoryDiagramRenderer>
 <DiagramLayerSettings yPosColumn="-1" linePlacementFlags="10" placement="2" dist="0" xPosColumn="-1" priority="0" obstacle="0" showAll="1"/>
 <editform></editform>
 <editforminit/>
 <featformsuppress>0</featformsuppress>
 <annotationform></annotationform>
 <editorlayout>tablayout</editorlayout>
 <excludeAttributesWMS/>
 <excludeAttributesWFS/>
 <attributeEditorForm>
  <attributeEditorContainer name="Manually entered">
   <attributeEditorField index="1" name="esu_id"/>
   <attributeEditorField index="3" name="usrn"/>
   <attributeEditorField index="4" name="rec_type"/>
   <attributeEditorField index="2" name="symbol"/>
   <attributeEditorField index="5" name="desc_text"/>
   <attributeEditorField index="6" name="locality"/>
   <attributeEditorField index="7" name="town"/>
   <attributeEditorField index="9" name="typ_3_usrn"/>
   <attributeEditorField index="10" name="typ_3_desc"/>
   <attributeEditorField index="11" name="typ_4_usrn"/>
   <attributeEditorField index="12" name="typ_4_desc"/>
  </attributeEditorContainer>
  <attributeEditorContainer name="Populated by RAMP">
   <attributeEditorField index="21" name="mcl_ref"/>
   <attributeEditorField index="8" name="entry_date"/>
   <attributeEditorField index="13" name="lor_ref_1"/>
   <attributeEditorField index="14" name="lor_ref_2"/>
   <attributeEditorField index="15" name="lor_desc"/>
   <attributeEditorField index="16" name="lane_number"/>
   <attributeEditorField index="17" name="speed_limit"/>
   <attributeEditorField index="18" name="rural_urban_id"/>
   <attributeEditorField index="19" name="section_type"/>
   <attributeEditorField index="22" name="street_classification"/>
   <attributeEditorField index="24" name="carriageway"/>
  </attributeEditorContainer>
  <attributeEditorContainer name="Legacy attributes">
   <attributeEditorField index="20" name="adoption_status"/>
   <attributeEditorField index="23" name="in_pilot"/>
  </attributeEditorContainer>
 </attributeEditorForm>
 <attributeactions/>
 <conditionalstyles>
  <rowstyles/>
  <fieldstyles/>
 </conditionalstyles>
</qgis>
','<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" xmlns:se="http://www.opengis.net/se">
 <NamedLayer>
  <se:Name>MCL</se:Name>
  <UserStyle>
   <se:Name>MCL</se:Name>
   <se:FeatureTypeStyle>
    <se:Rule>
     <se:Name>&lt;unassigned></se:Name>
     <se:Description>
      <se:Title>&lt;unassigned></se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>carriageway</ogc:PropertyName>
       <ogc:Literal></ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:LineSymbolizer>
      <se:Stroke>
       <se:SvgParameter name="stroke">#82d897</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.46</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
       <se:SvgParameter name="stroke-linecap">square</se:SvgParameter>
      </se:Stroke>
     </se:LineSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Dual</se:Name>
     <se:Description>
      <se:Title>Dual</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>carriageway</ogc:PropertyName>
       <ogc:Literal>Dual</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:LineSymbolizer>
      <se:Stroke>
       <se:SvgParameter name="stroke">#0d07a6</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.86</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
       <se:SvgParameter name="stroke-linecap">square</se:SvgParameter>
      </se:Stroke>
     </se:LineSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Single</se:Name>
     <se:Description>
      <se:Title>Single</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>carriageway</ogc:PropertyName>
       <ogc:Literal>Single</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:LineSymbolizer>
      <se:Stroke>
       <se:SvgParameter name="stroke">#fa3411</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.66</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
       <se:SvgParameter name="stroke-linecap">square</se:SvgParameter>
      </se:Stroke>
     </se:LineSymbolizer>
    </se:Rule>
   </se:FeatureTypeStyle>
  </UserStyle>
 </NamedLayer>
</StyledLayerDescriptor>
',1,'Tue Jun 7 15:44:00 2016',NULL,NULL,'2016-06-07 11:26:00');
INSERT INTO "layer_styles" VALUES(14,'roadnet_demo.sqlite','','rdpoly','geometry','hierarchy','<!DOCTYPE qgis PUBLIC ''http://mrcc.com/qgis.dtd'' ''SYSTEM''>
<qgis version="2.12.0-Lyon" minimumScale="0" maximumScale="1e+08" simplifyDrawingHints="1" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0">
 <edittypes>
  <edittype widgetv2type="TextEdit" name="PK_UID">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="symbol">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="rd_pol_id">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="element">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="hierarchy">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="ref_1">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="ref_2">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="desc_1">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="desc_2">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="desc_3">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="ref_3">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="currency_flag">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="part_label">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="label">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="label1">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="feature_length">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="r_usrn">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="mcl_cref">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
 </edittypes>
 <renderer-v2 attr="hierarchy" forceraster="0" symbollevels="0" type="categorizedSymbol">
  <categories>
   <category render="true" symbol="0" value="" label="&lt;not assigned>"/>
   <category render="true" symbol="1" value="LAF" label="Local Access Footway"/>
   <category render="true" symbol="2" value="LAR" label="Local Access Road"/>
   <category render="true" symbol="3" value="LF" label="Link Footway"/>
   <category render="true" symbol="4" value="LR" label="Link Road"/>
   <category render="true" symbol="5" value="MD" label="Main Distributor"/>
   <category render="true" symbol="6" value="MW" label="Motorway"/>
   <category render="true" symbol="7" value="PWR" label="Primary Walking Route"/>
   <category render="true" symbol="8" value="PWZ" label="Prestige Walking Zone"/>
   <category render="true" symbol="9" value="SD" label="Secondary Distributor"/>
   <category render="true" symbol="10" value="SR" label="Strategic Route"/>
   <category render="true" symbol="11" value="SS" label="Service Strip"/>
   <category render="true" symbol="12" value="SWR" label="Secondary Walking Route"/>
  </categories>
  <symbols>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="0">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="247,217,200,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="1">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,0,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="10">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,115,223,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="11">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,190,190,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.66"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="12">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="76,230,0,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="2">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,190,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="3">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="0,197,255,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="4">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="0,92,230,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="5">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="230,152,0,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="6">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="162,194,58,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="7">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,211,127,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="8">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="157,77,191,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="9">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="0,115,76,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
  </symbols>
  <source-symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="0">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="150,73,106,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
  </source-symbol>
  <rotation/>
  <sizescale scalemethod="diameter"/>
 </renderer-v2>
 <labeling type="rule-based">
  <rules>
   <rule scalemaxdenom="2500" description="Hierarchy" scalemindenom="10">
    <settings>
     <text-style fontItalic="0" fontFamily="Noto Sans" fontLetterSpacing="0" fontUnderline="0" fontSizeMapUnitMaxScale="0" fontWeight="50" fontStrikeout="0" textTransp="0" previewBkgrdColor="#ffffff" fontCapitals="0" textColor="0,0,0,255" fontSizeMapUnitMinScale="0" fontSizeInMapUnits="0" isExpression="1" blendMode="0" fontSize="11" fieldName=" concat(&quot;part_label&quot;, &quot;label1&quot;)" namedStyle="Regular" fontWordSpacing="0"/>
     <text-format placeDirectionSymbol="0" multilineAlign="0" rightDirectionSymbol=">" multilineHeight="1" plussign="0" addDirectionSymbol="0" leftDirectionSymbol="&lt;" formatNumbers="0" decimals="3" wrapChar="" reverseDirectionSymbol="0"/>
     <text-buffer bufferSize="1.6" bufferSizeMapUnitMinScale="0" bufferColor="255,255,190,255" bufferDraw="1" bufferBlendMode="0" bufferTransp="38" bufferSizeInMapUnits="0" bufferSizeMapUnitMaxScale="0" bufferNoFill="0" bufferJoinStyle="64"/>
     <background shapeSizeUnits="1" shapeType="0" shapeOffsetMapUnitMinScale="0" shapeSizeMapUnitMinScale="0" shapeSVGFile="" shapeOffsetX="0" shapeOffsetY="0" shapeBlendMode="0" shapeBorderWidthMapUnitMaxScale="0" shapeFillColor="255,255,255,255" shapeTransparency="0" shapeSizeType="0" shapeJoinStyle="64" shapeDraw="0" shapeSizeMapUnitMaxScale="0" shapeBorderWidthUnits="1" shapeSizeX="0" shapeSizeY="0" shapeRadiiX="0" shapeOffsetMapUnitMaxScale="0" shapeOffsetUnits="1" shapeRadiiY="0" shapeRotation="0" shapeBorderWidth="0" shapeRadiiMapUnitMinScale="0" shapeRadiiMapUnitMaxScale="0" shapeBorderColor="128,128,128,255" shapeRotationType="0" shapeRadiiUnits="1" shapeBorderWidthMapUnitMinScale="0"/>
     <shadow shadowOffsetGlobal="1" shadowRadiusUnits="1" shadowRadiusMapUnitMinScale="0" shadowTransparency="30" shadowColor="0,0,0,255" shadowUnder="0" shadowScale="100" shadowOffsetDist="1" shadowOffsetMapUnitMinScale="0" shadowRadiusMapUnitMaxScale="0" shadowDraw="0" shadowOffsetAngle="135" shadowRadius="1.5" shadowBlendMode="6" shadowOffsetMapUnitMaxScale="0" shadowRadiusAlphaOnly="0" shadowOffsetUnits="1"/>
     <placement repeatDistanceUnit="1" placement="0" maxCurvedCharAngleIn="20" repeatDistance="0" distMapUnitMaxScale="0" labelOffsetMapUnitMaxScale="0" distInMapUnits="0" labelOffsetInMapUnits="1" xOffset="0" preserveRotation="1" centroidWhole="0" priority="5" repeatDistanceMapUnitMaxScale="0" yOffset="0" placementFlags="10" repeatDistanceMapUnitMinScale="0" centroidInside="0" dist="0" angleOffset="0" maxCurvedCharAngleOut="-20" fitInPolygonOnly="0" quadOffset="4" distMapUnitMinScale="0" labelOffsetMapUnitMinScale="0"/>
     <rendering fontMinPixelSize="3" scaleMax="10000000" fontMaxPixelSize="10000" scaleMin="1" upsidedownLabels="0" limitNumLabels="0" obstacle="1" obstacleFactor="1" scaleVisibility="0" fontLimitPixelSize="0" mergeLines="0" obstacleType="0" labelPerPart="0" maxNumLabels="2000" displayAll="0" minFeatureSize="0"/>
     <data-defined/>
    </settings>
   </rule>
  </rules>
 </labeling>
 <customproperties>
  <property key="labeling/addDirectionSymbol" value="false"/>
  <property key="labeling/angleOffset" value="0"/>
  <property key="labeling/blendMode" value="0"/>
  <property key="labeling/bufferBlendMode" value="0"/>
  <property key="labeling/bufferColorA" value="255"/>
  <property key="labeling/bufferColorB" value="255"/>
  <property key="labeling/bufferColorG" value="255"/>
  <property key="labeling/bufferColorR" value="255"/>
  <property key="labeling/bufferDraw" value="false"/>
  <property key="labeling/bufferJoinStyle" value="64"/>
  <property key="labeling/bufferNoFill" value="false"/>
  <property key="labeling/bufferSize" value="1"/>
  <property key="labeling/bufferSizeInMapUnits" value="false"/>
  <property key="labeling/bufferSizeMapUnitMaxScale" value="0"/>
  <property key="labeling/bufferSizeMapUnitMinScale" value="0"/>
  <property key="labeling/bufferTransp" value="0"/>
  <property key="labeling/centroidInside" value="false"/>
  <property key="labeling/centroidWhole" value="false"/>
  <property key="labeling/decimals" value="3"/>
  <property key="labeling/displayAll" value="false"/>
  <property key="labeling/dist" value="0"/>
  <property key="labeling/distInMapUnits" value="false"/>
  <property key="labeling/distMapUnitMaxScale" value="0"/>
  <property key="labeling/distMapUnitMinScale" value="0"/>
  <property key="labeling/drawLabels" value="false"/>
  <property key="labeling/enabled" value="false"/>
  <property key="labeling/fieldName" value=""/>
  <property key="labeling/fitInPolygonOnly" value="false"/>
  <property key="labeling/fontCapitals" value="0"/>
  <property key="labeling/fontFamily" value="Noto Sans"/>
  <property key="labeling/fontItalic" value="false"/>
  <property key="labeling/fontLetterSpacing" value="0"/>
  <property key="labeling/fontLimitPixelSize" value="false"/>
  <property key="labeling/fontMaxPixelSize" value="10000"/>
  <property key="labeling/fontMinPixelSize" value="3"/>
  <property key="labeling/fontSize" value="9"/>
  <property key="labeling/fontSizeInMapUnits" value="false"/>
  <property key="labeling/fontSizeMapUnitMaxScale" value="0"/>
  <property key="labeling/fontSizeMapUnitMinScale" value="0"/>
  <property key="labeling/fontStrikeout" value="false"/>
  <property key="labeling/fontUnderline" value="false"/>
  <property key="labeling/fontWeight" value="50"/>
  <property key="labeling/fontWordSpacing" value="0"/>
  <property key="labeling/formatNumbers" value="false"/>
  <property key="labeling/isExpression" value="true"/>
  <property key="labeling/labelOffsetInMapUnits" value="true"/>
  <property key="labeling/labelOffsetMapUnitMaxScale" value="0"/>
  <property key="labeling/labelOffsetMapUnitMinScale" value="0"/>
  <property key="labeling/labelPerPart" value="false"/>
  <property key="labeling/leftDirectionSymbol" value="&lt;"/>
  <property key="labeling/limitNumLabels" value="false"/>
  <property key="labeling/maxCurvedCharAngleIn" value="20"/>
  <property key="labeling/maxCurvedCharAngleOut" value="-20"/>
  <property key="labeling/maxNumLabels" value="2000"/>
  <property key="labeling/mergeLines" value="false"/>
  <property key="labeling/minFeatureSize" value="0"/>
  <property key="labeling/multilineAlign" value="0"/>
  <property key="labeling/multilineHeight" value="1"/>
  <property key="labeling/namedStyle" value="Regular"/>
  <property key="labeling/obstacle" value="true"/>
  <property key="labeling/obstacleFactor" value="1"/>
  <property key="labeling/obstacleType" value="0"/>
  <property key="labeling/placeDirectionSymbol" value="0"/>
  <property key="labeling/placement" value="1"/>
  <property key="labeling/placementFlags" value="10"/>
  <property key="labeling/plussign" value="false"/>
  <property key="labeling/preserveRotation" value="true"/>
  <property key="labeling/previewBkgrdColor" value="#ffffff"/>
  <property key="labeling/priority" value="5"/>
  <property key="labeling/quadOffset" value="4"/>
  <property key="labeling/repeatDistance" value="0"/>
  <property key="labeling/repeatDistanceMapUnitMaxScale" value="0"/>
  <property key="labeling/repeatDistanceMapUnitMinScale" value="0"/>
  <property key="labeling/repeatDistanceUnit" value="1"/>
  <property key="labeling/reverseDirectionSymbol" value="false"/>
  <property key="labeling/rightDirectionSymbol" value=">"/>
  <property key="labeling/scaleMax" value="10000000"/>
  <property key="labeling/scaleMin" value="1"/>
  <property key="labeling/scaleVisibility" value="false"/>
  <property key="labeling/shadowBlendMode" value="6"/>
  <property key="labeling/shadowColorB" value="0"/>
  <property key="labeling/shadowColorG" value="0"/>
  <property key="labeling/shadowColorR" value="0"/>
  <property key="labeling/shadowDraw" value="false"/>
  <property key="labeling/shadowOffsetAngle" value="135"/>
  <property key="labeling/shadowOffsetDist" value="1"/>
  <property key="labeling/shadowOffsetGlobal" value="true"/>
  <property key="labeling/shadowOffsetMapUnitMaxScale" value="0"/>
  <property key="labeling/shadowOffsetMapUnitMinScale" value="0"/>
  <property key="labeling/shadowOffsetUnits" value="1"/>
  <property key="labeling/shadowRadius" value="1.5"/>
  <property key="labeling/shadowRadiusAlphaOnly" value="false"/>
  <property key="labeling/shadowRadiusMapUnitMaxScale" value="0"/>
  <property key="labeling/shadowRadiusMapUnitMinScale" value="0"/>
  <property key="labeling/shadowRadiusUnits" value="1"/>
  <property key="labeling/shadowScale" value="100"/>
  <property key="labeling/shadowTransparency" value="30"/>
  <property key="labeling/shadowUnder" value="0"/>
  <property key="labeling/shapeBlendMode" value="0"/>
  <property key="labeling/shapeBorderColorA" value="255"/>
  <property key="labeling/shapeBorderColorB" value="128"/>
  <property key="labeling/shapeBorderColorG" value="128"/>
  <property key="labeling/shapeBorderColorR" value="128"/>
  <property key="labeling/shapeBorderWidth" value="0"/>
  <property key="labeling/shapeBorderWidthMapUnitMaxScale" value="0"/>
  <property key="labeling/shapeBorderWidthMapUnitMinScale" value="0"/>
  <property key="labeling/shapeBorderWidthUnits" value="1"/>
  <property key="labeling/shapeDraw" value="false"/>
  <property key="labeling/shapeFillColorA" value="255"/>
  <property key="labeling/shapeFillColorB" value="255"/>
  <property key="labeling/shapeFillColorG" value="255"/>
  <property key="labeling/shapeFillColorR" value="255"/>
  <property key="labeling/shapeJoinStyle" value="64"/>
  <property key="labeling/shapeOffsetMapUnitMaxScale" value="0"/>
  <property key="labeling/shapeOffsetMapUnitMinScale" value="0"/>
  <property key="labeling/shapeOffsetUnits" value="1"/>
  <property key="labeling/shapeOffsetX" value="0"/>
  <property key="labeling/shapeOffsetY" value="0"/>
  <property key="labeling/shapeRadiiMapUnitMaxScale" value="0"/>
  <property key="labeling/shapeRadiiMapUnitMinScale" value="0"/>
  <property key="labeling/shapeRadiiUnits" value="1"/>
  <property key="labeling/shapeRadiiX" value="0"/>
  <property key="labeling/shapeRadiiY" value="0"/>
  <property key="labeling/shapeRotation" value="0"/>
  <property key="labeling/shapeRotationType" value="0"/>
  <property key="labeling/shapeSVGFile" value=""/>
  <property key="labeling/shapeSizeMapUnitMaxScale" value="0"/>
  <property key="labeling/shapeSizeMapUnitMinScale" value="0"/>
  <property key="labeling/shapeSizeType" value="0"/>
  <property key="labeling/shapeSizeUnits" value="1"/>
  <property key="labeling/shapeSizeX" value="0"/>
  <property key="labeling/shapeSizeY" value="0"/>
  <property key="labeling/shapeTransparency" value="0"/>
  <property key="labeling/shapeType" value="0"/>
  <property key="labeling/textColorA" value="255"/>
  <property key="labeling/textColorB" value="0"/>
  <property key="labeling/textColorG" value="0"/>
  <property key="labeling/textColorR" value="0"/>
  <property key="labeling/textTransp" value="0"/>
  <property key="labeling/upsidedownLabels" value="0"/>
  <property key="labeling/wrapChar" value=""/>
  <property key="labeling/xOffset" value="0"/>
  <property key="labeling/yOffset" value="0"/>
  <property key="variableNames" value="_fields_"/>
  <property key="variableValues" value=""/>
 </customproperties>
 <blendMode>0</blendMode>
 <featureBlendMode>0</featureBlendMode>
 <layerTransparency>0</layerTransparency>
 <displayfield>PK_UID</displayfield>
 <label>0</label>
 <labelattributes>
  <label fieldname="" text="Label"/>
  <family fieldname="" name="Noto Sans"/>
  <size fieldname="" units="pt" value="12"/>
  <bold fieldname="" on="0"/>
  <italic fieldname="" on="0"/>
  <underline fieldname="" on="0"/>
  <strikeout fieldname="" on="0"/>
  <color fieldname="" red="0" blue="0" green="0"/>
  <x fieldname=""/>
  <y fieldname=""/>
  <offset x="0" y="0" units="pt" yfieldname="" xfieldname=""/>
  <angle fieldname="" value="0" auto="0"/>
  <alignment fieldname="" value="center"/>
  <buffercolor fieldname="" red="255" blue="255" green="255"/>
  <buffersize fieldname="" units="pt" value="1"/>
  <bufferenabled fieldname="" on=""/>
  <multilineenabled fieldname="" on=""/>
  <selectedonly on=""/>
 </labelattributes>
 <SingleCategoryDiagramRenderer diagramType="Pie">
  <DiagramCategory penColor="#000000" labelPlacementMethod="XHeight" penWidth="0" diagramOrientation="Up" minimumSize="0" barWidth="5" penAlpha="255" maxScaleDenominator="1e+08" backgroundColor="#ffffff" transparency="0" width="15" scaleDependency="Area" backgroundAlpha="255" angleOffset="1440" scaleBasedVisibility="0" enabled="0" height="15" sizeType="MM" minScaleDenominator="-4.65661e-10">
   <fontProperties description="Noto Sans,9,-1,5,50,0,0,0,0,0" style=""/>
   <attribute field="" color="#000000" label=""/>
  </DiagramCategory>
 </SingleCategoryDiagramRenderer>
 <DiagramLayerSettings yPosColumn="-1" linePlacementFlags="10" placement="0" dist="0" xPosColumn="-1" priority="0" obstacle="0" showAll="1"/>
 <editform></editform>
 <editforminit/>
 <featformsuppress>0</featformsuppress>
 <annotationform></annotationform>
 <editorlayout>generatedlayout</editorlayout>
 <excludeAttributesWMS/>
 <excludeAttributesWFS/>
 <attributeactions/>
 <conditionalstyles>
  <rowstyles/>
  <fieldstyles/>
 </conditionalstyles>
</qgis>
','<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" xmlns:se="http://www.opengis.net/se">
 <NamedLayer>
  <se:Name>Hierarchy</se:Name>
  <UserStyle>
   <se:Name>Hierarchy</se:Name>
   <se:FeatureTypeStyle>
    <se:Rule>
     <se:Name>&lt;not assigned></se:Name>
     <se:Description>
      <se:Title>&lt;not assigned></se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>hierarchy</ogc:PropertyName>
       <ogc:Literal></ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#f7d9c8</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Local Access Footway</se:Name>
     <se:Description>
      <se:Title>Local Access Footway</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>hierarchy</ogc:PropertyName>
       <ogc:Literal>LAF</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#ffff00</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Local Access Road</se:Name>
     <se:Description>
      <se:Title>Local Access Road</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>hierarchy</ogc:PropertyName>
       <ogc:Literal>LAR</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#ffffbe</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Link Footway</se:Name>
     <se:Description>
      <se:Title>Link Footway</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>hierarchy</ogc:PropertyName>
       <ogc:Literal>LF</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#00c5ff</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Link Road</se:Name>
     <se:Description>
      <se:Title>Link Road</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>hierarchy</ogc:PropertyName>
       <ogc:Literal>LR</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#005ce6</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Main Distributor</se:Name>
     <se:Description>
      <se:Title>Main Distributor</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>hierarchy</ogc:PropertyName>
       <ogc:Literal>MD</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#e69800</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Motorway</se:Name>
     <se:Description>
      <se:Title>Motorway</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>hierarchy</ogc:PropertyName>
       <ogc:Literal>MW</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#a2c23a</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Primary Walking Route</se:Name>
     <se:Description>
      <se:Title>Primary Walking Route</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>hierarchy</ogc:PropertyName>
       <ogc:Literal>PWR</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#ffd37f</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Prestige Walking Zone</se:Name>
     <se:Description>
      <se:Title>Prestige Walking Zone</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>hierarchy</ogc:PropertyName>
       <ogc:Literal>PWZ</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#9d4dbf</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Secondary Distributor</se:Name>
     <se:Description>
      <se:Title>Secondary Distributor</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>hierarchy</ogc:PropertyName>
       <ogc:Literal>SD</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#00734c</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Strategic Route</se:Name>
     <se:Description>
      <se:Title>Strategic Route</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>hierarchy</ogc:PropertyName>
       <ogc:Literal>SR</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#ff73df</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Service Strip</se:Name>
     <se:Description>
      <se:Title>Service Strip</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>hierarchy</ogc:PropertyName>
       <ogc:Literal>SS</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#ffbebe</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.66</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Secondary Walking Route</se:Name>
     <se:Description>
      <se:Title>Secondary Walking Route</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>hierarchy</ogc:PropertyName>
       <ogc:Literal>SWR</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#4ce600</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
   </se:FeatureTypeStyle>
  </UserStyle>
 </NamedLayer>
</StyledLayerDescriptor>
',1,'Tue Jun 7 16:04:29 2016',NULL,NULL,'2016-06-07 15:04:29');
INSERT INTO "layer_styles" VALUES(15,'roadnet_demo.sqlite','','rdpoly','geometry','element','<!DOCTYPE qgis PUBLIC ''http://mrcc.com/qgis.dtd'' ''SYSTEM''>
<qgis version="2.12.0-Lyon" minimumScale="-4.65661e-10" maximumScale="1e+08" simplifyDrawingHints="1" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0">
 <edittypes>
  <edittype widgetv2type="TextEdit" name="PK_UID">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="symbol">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="rd_pol_id">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="element">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="hierarchy">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="ref_1">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="ref_2">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="desc_1">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="desc_2">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="desc_3">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="ref_3">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="currency_flag">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="part_label">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="label">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="label1">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="feature_length">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="r_usrn">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
  <edittype widgetv2type="TextEdit" name="mcl_cref">
   <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
  </edittype>
 </edittypes>
 <renderer-v2 attr="element" forceraster="0" symbollevels="0" type="categorizedSymbol">
  <categories>
   <category render="true" symbol="0" value="ACARPK" label="Adopted Carpark"/>
   <category render="true" symbol="1" value="CARPK" label="Parking"/>
   <category render="true" symbol="2" value="CGWAY" label="Carriageway"/>
   <category render="true" symbol="3" value="CRESERVE" label="Central Reserve"/>
   <category render="true" symbol="4" value="FPATH" label="Footpath"/>
   <category render="true" symbol="5" value="FTWAY" label="Footway"/>
   <category render="true" symbol="6" value="LSHARD" label="Landscaping (Hard)"/>
   <category render="true" symbol="7" value="LSSOFT" label="Landscaping (Soft)"/>
   <category render="true" symbol="8" value="" label="&lt;not assigned>"/>
   <category render="true" symbol="9" value="SSTRIP" label="Service Strip"/>
   <category render="true" symbol="10" value="VERGE" label="Verge"/>
   <category render="true" symbol="11" value="CYCLE" label="Cycleway / Path"/>
  </categories>
  <symbols>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="0">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="147,199,42,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="1">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="46,76,176,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="10">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="173,102,69,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="11">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="126,168,168,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="2">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="178,178,178,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="3">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="89,156,62,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="4">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="230,152,0,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="5">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="223,115,255,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="6">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="143,48,201,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="7">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="166,156,66,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="8">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="247,217,200,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="9">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="179,45,71,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
  </symbols>
  <source-symbol>
   <symbol alpha="1" clip_to_extent="1" type="fill" name="0">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="150,73,106,255"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.26"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
  </source-symbol>
  <rotation/>
  <sizescale scalemethod="diameter"/>
 </renderer-v2>
 <labeling type="rule-based">
  <rules>
   <rule scalemaxdenom="2500" description="Element" scalemindenom="10">
    <settings>
     <text-style fontItalic="0" fontFamily="Noto Sans" fontLetterSpacing="0" fontUnderline="0" fontSizeMapUnitMaxScale="0" fontWeight="50" fontStrikeout="0" textTransp="0" previewBkgrdColor="#ffffff" fontCapitals="0" textColor="0,0,0,255" fontSizeMapUnitMinScale="0" fontSizeInMapUnits="0" isExpression="1" blendMode="0" fontSize="11" fieldName="concat( &quot;part_label&quot; , &quot;label&quot; )" namedStyle="Regular" fontWordSpacing="0"/>
     <text-format placeDirectionSymbol="0" multilineAlign="0" rightDirectionSymbol=">" multilineHeight="1" plussign="0" addDirectionSymbol="0" leftDirectionSymbol="&lt;" formatNumbers="0" decimals="3" wrapChar="" reverseDirectionSymbol="0"/>
     <text-buffer bufferSize="1.6" bufferSizeMapUnitMinScale="0" bufferColor="255,255,190,255" bufferDraw="1" bufferBlendMode="0" bufferTransp="40" bufferSizeInMapUnits="0" bufferSizeMapUnitMaxScale="0" bufferNoFill="0" bufferJoinStyle="64"/>
     <background shapeSizeUnits="1" shapeType="0" shapeOffsetMapUnitMinScale="0" shapeSizeMapUnitMinScale="0" shapeSVGFile="" shapeOffsetX="0" shapeOffsetY="0" shapeBlendMode="0" shapeBorderWidthMapUnitMaxScale="0" shapeFillColor="255,255,255,255" shapeTransparency="0" shapeSizeType="0" shapeJoinStyle="64" shapeDraw="0" shapeSizeMapUnitMaxScale="0" shapeBorderWidthUnits="1" shapeSizeX="0" shapeSizeY="0" shapeRadiiX="0" shapeOffsetMapUnitMaxScale="0" shapeOffsetUnits="1" shapeRadiiY="0" shapeRotation="0" shapeBorderWidth="0" shapeRadiiMapUnitMinScale="0" shapeRadiiMapUnitMaxScale="0" shapeBorderColor="128,128,128,255" shapeRotationType="0" shapeRadiiUnits="1" shapeBorderWidthMapUnitMinScale="0"/>
     <shadow shadowOffsetGlobal="1" shadowRadiusUnits="1" shadowRadiusMapUnitMinScale="0" shadowTransparency="30" shadowColor="0,0,0,255" shadowUnder="0" shadowScale="100" shadowOffsetDist="1" shadowOffsetMapUnitMinScale="0" shadowRadiusMapUnitMaxScale="0" shadowDraw="0" shadowOffsetAngle="135" shadowRadius="1.5" shadowBlendMode="6" shadowOffsetMapUnitMaxScale="0" shadowRadiusAlphaOnly="0" shadowOffsetUnits="1"/>
     <placement repeatDistanceUnit="1" placement="0" maxCurvedCharAngleIn="20" repeatDistance="0" distMapUnitMaxScale="0" labelOffsetMapUnitMaxScale="0" distInMapUnits="0" labelOffsetInMapUnits="1" xOffset="0" preserveRotation="1" centroidWhole="0" priority="5" repeatDistanceMapUnitMaxScale="0" yOffset="0" placementFlags="10" repeatDistanceMapUnitMinScale="0" centroidInside="0" dist="0" angleOffset="0" maxCurvedCharAngleOut="-20" fitInPolygonOnly="0" quadOffset="4" distMapUnitMinScale="0" labelOffsetMapUnitMinScale="0"/>
     <rendering fontMinPixelSize="3" scaleMax="10000000" fontMaxPixelSize="10000" scaleMin="1" upsidedownLabels="0" limitNumLabels="0" obstacle="1" obstacleFactor="1" scaleVisibility="0" fontLimitPixelSize="0" mergeLines="0" obstacleType="0" labelPerPart="0" maxNumLabels="2000" displayAll="0" minFeatureSize="0"/>
     <data-defined/>
    </settings>
   </rule>
  </rules>
 </labeling>
 <customproperties>
  <property key="labeling/addDirectionSymbol" value="false"/>
  <property key="labeling/angleOffset" value="0"/>
  <property key="labeling/blendMode" value="0"/>
  <property key="labeling/bufferBlendMode" value="0"/>
  <property key="labeling/bufferColorA" value="255"/>
  <property key="labeling/bufferColorB" value="255"/>
  <property key="labeling/bufferColorG" value="255"/>
  <property key="labeling/bufferColorR" value="255"/>
  <property key="labeling/bufferDraw" value="false"/>
  <property key="labeling/bufferJoinStyle" value="64"/>
  <property key="labeling/bufferNoFill" value="false"/>
  <property key="labeling/bufferSize" value="1"/>
  <property key="labeling/bufferSizeInMapUnits" value="false"/>
  <property key="labeling/bufferSizeMapUnitMaxScale" value="0"/>
  <property key="labeling/bufferSizeMapUnitMinScale" value="0"/>
  <property key="labeling/bufferTransp" value="0"/>
  <property key="labeling/centroidInside" value="false"/>
  <property key="labeling/centroidWhole" value="false"/>
  <property key="labeling/decimals" value="3"/>
  <property key="labeling/displayAll" value="false"/>
  <property key="labeling/dist" value="0"/>
  <property key="labeling/distInMapUnits" value="false"/>
  <property key="labeling/distMapUnitMaxScale" value="0"/>
  <property key="labeling/distMapUnitMinScale" value="0"/>
  <property key="labeling/drawLabels" value="false"/>
  <property key="labeling/enabled" value="false"/>
  <property key="labeling/fieldName" value=""/>
  <property key="labeling/fitInPolygonOnly" value="false"/>
  <property key="labeling/fontCapitals" value="0"/>
  <property key="labeling/fontFamily" value="Noto Sans"/>
  <property key="labeling/fontItalic" value="false"/>
  <property key="labeling/fontLetterSpacing" value="0"/>
  <property key="labeling/fontLimitPixelSize" value="false"/>
  <property key="labeling/fontMaxPixelSize" value="10000"/>
  <property key="labeling/fontMinPixelSize" value="3"/>
  <property key="labeling/fontSize" value="9"/>
  <property key="labeling/fontSizeInMapUnits" value="false"/>
  <property key="labeling/fontSizeMapUnitMaxScale" value="0"/>
  <property key="labeling/fontSizeMapUnitMinScale" value="0"/>
  <property key="labeling/fontStrikeout" value="false"/>
  <property key="labeling/fontUnderline" value="false"/>
  <property key="labeling/fontWeight" value="50"/>
  <property key="labeling/fontWordSpacing" value="0"/>
  <property key="labeling/formatNumbers" value="false"/>
  <property key="labeling/isExpression" value="true"/>
  <property key="labeling/labelOffsetInMapUnits" value="true"/>
  <property key="labeling/labelOffsetMapUnitMaxScale" value="0"/>
  <property key="labeling/labelOffsetMapUnitMinScale" value="0"/>
  <property key="labeling/labelPerPart" value="false"/>
  <property key="labeling/leftDirectionSymbol" value="&lt;"/>
  <property key="labeling/limitNumLabels" value="false"/>
  <property key="labeling/maxCurvedCharAngleIn" value="20"/>
  <property key="labeling/maxCurvedCharAngleOut" value="-20"/>
  <property key="labeling/maxNumLabels" value="2000"/>
  <property key="labeling/mergeLines" value="false"/>
  <property key="labeling/minFeatureSize" value="0"/>
  <property key="labeling/multilineAlign" value="0"/>
  <property key="labeling/multilineHeight" value="1"/>
  <property key="labeling/namedStyle" value="Regular"/>
  <property key="labeling/obstacle" value="true"/>
  <property key="labeling/obstacleFactor" value="1"/>
  <property key="labeling/obstacleType" value="0"/>
  <property key="labeling/placeDirectionSymbol" value="0"/>
  <property key="labeling/placement" value="1"/>
  <property key="labeling/placementFlags" value="10"/>
  <property key="labeling/plussign" value="false"/>
  <property key="labeling/preserveRotation" value="true"/>
  <property key="labeling/previewBkgrdColor" value="#ffffff"/>
  <property key="labeling/priority" value="5"/>
  <property key="labeling/quadOffset" value="4"/>
  <property key="labeling/repeatDistance" value="0"/>
  <property key="labeling/repeatDistanceMapUnitMaxScale" value="0"/>
  <property key="labeling/repeatDistanceMapUnitMinScale" value="0"/>
  <property key="labeling/repeatDistanceUnit" value="1"/>
  <property key="labeling/reverseDirectionSymbol" value="false"/>
  <property key="labeling/rightDirectionSymbol" value=">"/>
  <property key="labeling/scaleMax" value="10000000"/>
  <property key="labeling/scaleMin" value="1"/>
  <property key="labeling/scaleVisibility" value="false"/>
  <property key="labeling/shadowBlendMode" value="6"/>
  <property key="labeling/shadowColorB" value="0"/>
  <property key="labeling/shadowColorG" value="0"/>
  <property key="labeling/shadowColorR" value="0"/>
  <property key="labeling/shadowDraw" value="false"/>
  <property key="labeling/shadowOffsetAngle" value="135"/>
  <property key="labeling/shadowOffsetDist" value="1"/>
  <property key="labeling/shadowOffsetGlobal" value="true"/>
  <property key="labeling/shadowOffsetMapUnitMaxScale" value="0"/>
  <property key="labeling/shadowOffsetMapUnitMinScale" value="0"/>
  <property key="labeling/shadowOffsetUnits" value="1"/>
  <property key="labeling/shadowRadius" value="1.5"/>
  <property key="labeling/shadowRadiusAlphaOnly" value="false"/>
  <property key="labeling/shadowRadiusMapUnitMaxScale" value="0"/>
  <property key="labeling/shadowRadiusMapUnitMinScale" value="0"/>
  <property key="labeling/shadowRadiusUnits" value="1"/>
  <property key="labeling/shadowScale" value="100"/>
  <property key="labeling/shadowTransparency" value="30"/>
  <property key="labeling/shadowUnder" value="0"/>
  <property key="labeling/shapeBlendMode" value="0"/>
  <property key="labeling/shapeBorderColorA" value="255"/>
  <property key="labeling/shapeBorderColorB" value="128"/>
  <property key="labeling/shapeBorderColorG" value="128"/>
  <property key="labeling/shapeBorderColorR" value="128"/>
  <property key="labeling/shapeBorderWidth" value="0"/>
  <property key="labeling/shapeBorderWidthMapUnitMaxScale" value="0"/>
  <property key="labeling/shapeBorderWidthMapUnitMinScale" value="0"/>
  <property key="labeling/shapeBorderWidthUnits" value="1"/>
  <property key="labeling/shapeDraw" value="false"/>
  <property key="labeling/shapeFillColorA" value="255"/>
  <property key="labeling/shapeFillColorB" value="255"/>
  <property key="labeling/shapeFillColorG" value="255"/>
  <property key="labeling/shapeFillColorR" value="255"/>
  <property key="labeling/shapeJoinStyle" value="64"/>
  <property key="labeling/shapeOffsetMapUnitMaxScale" value="0"/>
  <property key="labeling/shapeOffsetMapUnitMinScale" value="0"/>
  <property key="labeling/shapeOffsetUnits" value="1"/>
  <property key="labeling/shapeOffsetX" value="0"/>
  <property key="labeling/shapeOffsetY" value="0"/>
  <property key="labeling/shapeRadiiMapUnitMaxScale" value="0"/>
  <property key="labeling/shapeRadiiMapUnitMinScale" value="0"/>
  <property key="labeling/shapeRadiiUnits" value="1"/>
  <property key="labeling/shapeRadiiX" value="0"/>
  <property key="labeling/shapeRadiiY" value="0"/>
  <property key="labeling/shapeRotation" value="0"/>
  <property key="labeling/shapeRotationType" value="0"/>
  <property key="labeling/shapeSVGFile" value=""/>
  <property key="labeling/shapeSizeMapUnitMaxScale" value="0"/>
  <property key="labeling/shapeSizeMapUnitMinScale" value="0"/>
  <property key="labeling/shapeSizeType" value="0"/>
  <property key="labeling/shapeSizeUnits" value="1"/>
  <property key="labeling/shapeSizeX" value="0"/>
  <property key="labeling/shapeSizeY" value="0"/>
  <property key="labeling/shapeTransparency" value="0"/>
  <property key="labeling/shapeType" value="0"/>
  <property key="labeling/textColorA" value="255"/>
  <property key="labeling/textColorB" value="0"/>
  <property key="labeling/textColorG" value="0"/>
  <property key="labeling/textColorR" value="0"/>
  <property key="labeling/textTransp" value="0"/>
  <property key="labeling/upsidedownLabels" value="0"/>
  <property key="labeling/wrapChar" value=""/>
  <property key="labeling/xOffset" value="0"/>
  <property key="labeling/yOffset" value="0"/>
  <property key="variableNames" value="_fields_"/>
  <property key="variableValues" value=""/>
 </customproperties>
 <blendMode>0</blendMode>
 <featureBlendMode>0</featureBlendMode>
 <layerTransparency>0</layerTransparency>
 <displayfield>PK_UID</displayfield>
 <label>0</label>
 <labelattributes>
  <label fieldname="" text="Label"/>
  <family fieldname="" name="Noto Sans"/>
  <size fieldname="" units="pt" value="12"/>
  <bold fieldname="" on="0"/>
  <italic fieldname="" on="0"/>
  <underline fieldname="" on="0"/>
  <strikeout fieldname="" on="0"/>
  <color fieldname="" red="0" blue="0" green="0"/>
  <x fieldname=""/>
  <y fieldname=""/>
  <offset x="0" y="0" units="pt" yfieldname="" xfieldname=""/>
  <angle fieldname="" value="0" auto="0"/>
  <alignment fieldname="" value="center"/>
  <buffercolor fieldname="" red="255" blue="255" green="255"/>
  <buffersize fieldname="" units="pt" value="1"/>
  <bufferenabled fieldname="" on=""/>
  <multilineenabled fieldname="" on=""/>
  <selectedonly on=""/>
 </labelattributes>
 <SingleCategoryDiagramRenderer diagramType="Pie">
  <DiagramCategory penColor="#000000" labelPlacementMethod="XHeight" penWidth="0" diagramOrientation="Up" minimumSize="0" barWidth="5" penAlpha="255" maxScaleDenominator="1e+08" backgroundColor="#ffffff" transparency="0" width="15" scaleDependency="Area" backgroundAlpha="255" angleOffset="1440" scaleBasedVisibility="0" enabled="0" height="15" sizeType="MM" minScaleDenominator="0">
   <fontProperties description="Noto Sans,9,-1,5,50,0,0,0,0,0" style=""/>
   <attribute field="" color="#000000" label=""/>
  </DiagramCategory>
 </SingleCategoryDiagramRenderer>
 <DiagramLayerSettings yPosColumn="-1" linePlacementFlags="10" placement="0" dist="0" xPosColumn="-1" priority="0" obstacle="0" showAll="1"/>
 <editform></editform>
 <editforminit/>
 <featformsuppress>0</featformsuppress>
 <annotationform></annotationform>
 <editorlayout>generatedlayout</editorlayout>
 <excludeAttributesWMS/>
 <excludeAttributesWFS/>
 <attributeactions/>
 <conditionalstyles>
  <rowstyles/>
  <fieldstyles/>
 </conditionalstyles>
</qgis>
','<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" xmlns:se="http://www.opengis.net/se">
 <NamedLayer>
  <se:Name>Element</se:Name>
  <UserStyle>
   <se:Name>Element</se:Name>
   <se:FeatureTypeStyle>
    <se:Rule>
     <se:Name>Adopted Carpark</se:Name>
     <se:Description>
      <se:Title>Adopted Carpark</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>element</ogc:PropertyName>
       <ogc:Literal>ACARPK</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#93c72a</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Parking</se:Name>
     <se:Description>
      <se:Title>Parking</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>element</ogc:PropertyName>
       <ogc:Literal>CARPK</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#2e4cb0</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Carriageway</se:Name>
     <se:Description>
      <se:Title>Carriageway</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>element</ogc:PropertyName>
       <ogc:Literal>CGWAY</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#b2b2b2</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Central Reserve</se:Name>
     <se:Description>
      <se:Title>Central Reserve</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>element</ogc:PropertyName>
       <ogc:Literal>CRESERVE</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#599c3e</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Footpath</se:Name>
     <se:Description>
      <se:Title>Footpath</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>element</ogc:PropertyName>
       <ogc:Literal>FPATH</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#e69800</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Footway</se:Name>
     <se:Description>
      <se:Title>Footway</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>element</ogc:PropertyName>
       <ogc:Literal>FTWAY</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#df73ff</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Landscaping (Hard)</se:Name>
     <se:Description>
      <se:Title>Landscaping (Hard)</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>element</ogc:PropertyName>
       <ogc:Literal>LSHARD</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#8f30c9</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Landscaping (Soft)</se:Name>
     <se:Description>
      <se:Title>Landscaping (Soft)</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>element</ogc:PropertyName>
       <ogc:Literal>LSSOFT</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#a69c42</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>&lt;not assigned></se:Name>
     <se:Description>
      <se:Title>&lt;not assigned></se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>element</ogc:PropertyName>
       <ogc:Literal></ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#f7d9c8</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Service Strip</se:Name>
     <se:Description>
      <se:Title>Service Strip</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>element</ogc:PropertyName>
       <ogc:Literal>SSTRIP</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#b32d47</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Verge</se:Name>
     <se:Description>
      <se:Title>Verge</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>element</ogc:PropertyName>
       <ogc:Literal>VERGE</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#ad6645</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name>Cycleway / Path</se:Name>
     <se:Description>
      <se:Title>Cycleway / Path</se:Title>
     </se:Description>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:PropertyIsEqualTo>
       <ogc:PropertyName>element</ogc:PropertyName>
       <ogc:Literal>CYCLE</ogc:Literal>
      </ogc:PropertyIsEqualTo>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:SvgParameter name="fill">#7ea8a8</se:SvgParameter>
      </se:Fill>
      <se:Stroke>
       <se:SvgParameter name="stroke">#000000</se:SvgParameter>
       <se:SvgParameter name="stroke-width">0.26</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
      </se:Stroke>
     </se:PolygonSymbolizer>
    </se:Rule>
   </se:FeatureTypeStyle>
  </UserStyle>
 </NamedLayer>
</StyledLayerDescriptor>
',1,'Mon Jun 13 14:30:35 2016',NULL,NULL,'2016-06-13 13:30:35');
"""

populate_lookup_tables = """
INSERT INTO "tlkpSPEC_DES" VALUES(1,1,'Protected Road','Date Designated','Date');
INSERT INTO "tlkpSPEC_DES" VALUES(2,2,'Traffic Sensitive','Date Designated','Date');
INSERT INTO "tlkpSPEC_DES" VALUES(3,3,'Special Engineering Difficulty','Date Designated','SWA_Org_Ref,  Description, Date');
INSERT INTO "tlkpSPEC_DES" VALUES(4,4,'Restriction following Substantial Works','Date of Cessation','Date');
INSERT INTO "tlkpSPEC_DES" VALUES(5,5,'Unidentified Plant','','Description');
INSERT INTO "tlkpSPEC_DES" VALUES(6,6,'Sect144 Notice (Cost Sharing)','Date when Notice','Date');
INSERT INTO "tlkpSPEC_DES" VALUES(7,7,'Level Crossing','','SWA_Org_Ref');
INSERT INTO "tlkpSPEC_DES" VALUES(8,8,'Bridge  (NOT Special engineering dif)','','SWA_Org_Ref');
INSERT INTO "tlkpSPEC_DES" VALUES(9,9,'Road Trees','','');
INSERT INTO "tlkpSPEC_DES" VALUES(10,10,'Other Structure','','SWA_Org_Ref');
INSERT INTO "tlkpSPEC_DES" VALUES(11,11,'Conservation Designation','','SWA_Org_Ref,  Description');
INSERT INTO "tlkpSPEC_DES" VALUES(12,12,'Loops etc in Road surface','','SWA_Org_Ref,  Description');
INSERT INTO "tlkpSPEC_DES" VALUES(13,13,'Pedestrian Crossings','','');
INSERT INTO "tlkpSPEC_DES" VALUES(14,14,'Service Strips',NULL,'SWA_Org_Ref,  Description');
INSERT INTO "tlkpSPEC_DES" VALUES(15,15,'Private Apparatus',NULL,'SWA_Org_Ref,  Description');
INSERT INTO "tlkpSPEC_DES" VALUES(16,16,'Traffic Calming Features',NULL,'SWA_Org_Ref,  Description');
INSERT INTO "tlkpSPEC_DES" VALUES(17,17,'Traffic Signals',NULL,'SWA_Org_Ref,  Description');
INSERT INTO "tlkpSPEC_DES" VALUES(18,18,'Network Rail Level Crossing/Precautionary Area',NULL,NULL);
INSERT INTO "tlkpSPEC_DES" VALUES(19,19,'Traffic Sensitive Side Road',NULL,NULL);
INSERT INTO "tlkpSTREET_STATE" VALUES(1,0,'Unknown');
INSERT INTO "tlkpSTREET_STATE" VALUES(2,1,'Under construction');
INSERT INTO "tlkpSTREET_STATE" VALUES(3,2,'Open');
INSERT INTO "tlkpSTREET_STATE" VALUES(4,3,'Temporarily stopped up');
INSERT INTO "tlkpSTREET_STATE" VALUES(5,4,'Permanently closed');
INSERT INTO "tlkpSTREET_STATE" VALUES(6,5,'Open with restriction');
INSERT INTO "tlkpSTREET_CLASS" VALUES(1,0,'Undefined');
INSERT INTO "tlkpSTREET_CLASS" VALUES(2,4,'Pedestrian way or footpath');
INSERT INTO "tlkpSTREET_CLASS" VALUES(3,6,'Cycletrack or cycleway');
INSERT INTO "tlkpSTREET_CLASS" VALUES(4,8,'Open to vehicles');
INSERT INTO "tlkpSTREET_CLASS" VALUES(5,9,'Restricted access to vehicles');
INSERT INTO "tlkpREINS_CAT" VALUES(1,0,'00 - c/w special type (> 30msa)',1);
INSERT INTO "tlkpREINS_CAT" VALUES(2,1,'01 - c/w type 1 (10 - 30msa)',1);
INSERT INTO "tlkpREINS_CAT" VALUES(3,2,'02 - c/w type 2 (2.5 - 10msa)',1);
INSERT INTO "tlkpREINS_CAT" VALUES(4,3,'03 - c/w type 3 (0.5 - 2.5msa)',1);
INSERT INTO "tlkpREINS_CAT" VALUES(5,4,'04 - c/w type 4 (< 0.5msa)',1);
INSERT INTO "tlkpREINS_CAT" VALUES(6,5,'05 - high duty footway/path',2);
INSERT INTO "tlkpREINS_CAT" VALUES(7,6,'06 - high amenity footway/path',2);
INSERT INTO "tlkpREINS_CAT" VALUES(8,7,'07 - other/standard footway/path',2);
INSERT INTO "tlkpREINS_CAT" VALUES(9,8,'08 - unused',0);
INSERT INTO "tlkpREINS_CAT" VALUES(10,9,'09 - unused',0);
INSERT INTO "tlkpREINS_CAT" VALUES(11,10,'10 - c/w friction coatings',3);
INSERT INTO "tlkpREINS_CAT" VALUES(12,11,'11 - c/w coloured surfacings',3);
INSERT INTO "tlkpREINS_CAT" VALUES(13,12,'12 - c/w porous asphalt',3);
INSERT INTO "tlkpREINS_CAT" VALUES(14,13,'13 - high amenity carriageway',1);
INSERT INTO "tlkpROAD_STATUS" VALUES(1,0,' - none -');
INSERT INTO "tlkpROAD_STATUS" VALUES(2,1,'Public Road');
INSERT INTO "tlkpROAD_STATUS" VALUES(3,2,'Prospective Public Road');
INSERT INTO "tlkpROAD_STATUS" VALUES(4,3,'Private Road');
INSERT INTO "tlkpROAD_STATUS" VALUES(5,4,'Trunk Road');
INSERT INTO "tlkpWHOLE_ROAD" VALUES(1,1,'Yes');
INSERT INTO "tlkpWHOLE_ROAD" VALUES(2,0,'No');
INSERT INTO "tlkpSTREET_REF_TYPE" VALUES(1,1,'Named Road (Type 1)');
INSERT INTO "tlkpSTREET_REF_TYPE" VALUES(2,2,'Unnamed / Described Rd (Type 2)');
INSERT INTO "tlkpSTREET_REF_TYPE" VALUES(3,3,'Numbered Road (Type 3)');
INSERT INTO "tlkpSTREET_REF_TYPE" VALUES(4,4,'Official Alias (Type 4)');
INSERT INTO "tlkpSTREET_REF_TYPE" VALUES(5,7,'Unknown');
INSERT INTO "tlkpSTREET_REF_TYPE" VALUES(6,8,'Set aside');
INSERT INTO "tlkpORG" VALUES(1,'6983','Trunk Road South East');
INSERT INTO "tlkpORG" VALUES(3,'7093','Network Rail');
INSERT INTO "tlkpORG" VALUES(5,'7187','British Waterways');
INSERT INTO "tlkpORG" VALUES(6,'7285','Historic Scotland');
INSERT INTO "tlkpORG" VALUES(7,'7286','Scottish Natural Heritage');
INSERT INTO "tlkpORG" VALUES(8,'7287','Scottish Wildlife Trust');
INSERT INTO "tlkpORG" VALUES(10,'9999','thinkWhere Authority');
INSERT INTO "tlkpORG" VALUES(11,'9998','Frontagers/Developers');
INSERT INTO "tlkpAUTHORITY" VALUES(1,0,'- none -');
INSERT INTO "tlkpAUTHORITY" VALUES(2,9999,'thinkWhere Authority');
"""
