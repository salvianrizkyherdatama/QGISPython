#Tell me where is the shp file
Adm_Kab = 'Paste your shp path file here' #Don't forget to clear ""
#example E:\Kuliah\Perkuliahan\Semester 5\Geologi Teknik\Praktikum\Acara 6 Pemetaan Geotek\Batas Desa.shp
#Make it active layer
layer = iface.addVectorLayer(Adm_Kab, '', 'ogr')


#Make sure the layer is active and start to calculate
if not layer :
    print("No layer selected.")
else :
    
  d = QgsDistanceArea()
  d.setEllipsoid('WGS84')
  
  #Layer Start Editing
  layer.startEditing()
  
  #add Field
  field_names = [field.name() for field in layer.fields()]
  
  if "area_km" not in field_names:
    layer.addAttribute(QgsField("area_km", QVariant.Double))
    
  if "perimeter_km" not in field_names:
    layer.addAttribute(QgsField("perimeter_km", QVariant.Double))
  if "percent" not in field_names :
    layer.addAttribute(QgsField("percent", QVariant.Double))
  layer.updateFields()
  
  #Calculate total area
  total_area_km = 0
  for f in layer.getFeatures():
      geom = f.geometry()
      measure = d.measureArea(geom)
      measure_km = d.convertAreaMeasurement(measure, QgsUnitTypes.AreaSquareKilometers)
      total_area_km += measure_km
  
  #Calculate area, perimeter, and percent area
  if total_area_km > 0 :
   for f in layer.getFeatures():
  
      geom = f.geometry()
      
      #Calculate your area
      measure = d.measureArea(geom)
      measure_km = d.convertAreaMeasurement(measure, QgsUnitTypes.AreaSquareKilometers)
      
      #Calculate perimeter
      perimeter = d.measurePerimeter(geom)
      perimeter_km = d.convertLengthMeasurement(perimeter, QgsUnitTypes.DistanceKilometers)
      
      #Calculate Percent of Total Area
      percent_of_total = (measure_km/total_area_km) * 100 if total_area_km != 0 else 0
      
      #Update the Attribute Table with Perimeter and Area
      f.setAttribute(f.fieldNameIndex("area_km"), measure_km)
      f.setAttribute(f.fieldNameIndex("perimeter_km"), perimeter_km)
      f.setAttribute(f.fieldNameIndex("percent"), percent_of_total)
      layer.updateFeature(f)
      
   print("All done sir! Area, Perimeter, and Percentage Area have been added to the attribute table.")
      
  else :
      print("Total area is zero or invalid. Please check the geometries in your shapefile.")
      
layer.commitChanges()






#SRH