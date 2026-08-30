from risk_engine import calculate_flood_risk

rainfall=float(input("Enter rainfall data:"))
river_level=float(input("Enter river level data:"))
soil_moisture=float(input("Enter soil moisture data:"))
slope=float(input("Enter slope data:"))

risk_result=calculate_flood_risk(rainfall,river_level,soil_moisture,slope)
print(risk_result)