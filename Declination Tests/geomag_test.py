from geomag import declination

if __name__ == "__main__":
    # Latitude: 33.4213 Longitude: -111.9268
    latitude = 33.4213
    longitude = -111.9268

    
    
    print("Magnetic Declination Angle:", declination(latitude, longitude), "degrees")
