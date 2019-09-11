import json
from PIL import Image
import requests
from io import BytesIO
from io import StringIO
import PIL.ExifTags
def main():
    #open json turn it into string. coz it cannot be parsed directly
    file_string=""
    httpsString=list()
    with open("samplePhotoGPS.json") as json_file:
#        [
#    { "path": "https://raw.githubusercontent.com/SiciHan/Algorithm-practices/master/DSCN0010.jpg"}
#]
         
        for line in json_file:
            indexOfStart=line.find("https")
            indexOfEnd=line.find("\"}")
            if indexOfStart!=-1:
                url=line[indexOfStart:indexOfEnd]
                httpsString.append(url)
    # open img from each url link
    for url in httpsString:
        print("requesting image")
        print(url)
        response = requests.get(url)
        print("opening image")
        rc=response.content    
        img = Image.open(BytesIO(rc))
        print("gotten image")
        exif_data = img._getexif()# dictionary, but key is numbers
        #turn number keys into words
        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
            }
        #print(exif)
        #print(exif["GPSInfo"])
        #latitude: 43:28:2.814 in DMS
        #Longtitude:11:53:6.455999 in DMS
        GPSInfo=exif["GPSInfo"]
        latitude=GPSInfo[2]
        longtitude=GPSInfo[4]
        print(latitude,longtitude)
        latitudeInDecimal=latitude[0][0]+latitude[1][0]/60
        longtitudeInDecimal=longtitude[0][0]+longtitude[1][0]/60
        res={"lat":latitudeInDecimal,"long":longtitudeInDecimal}
        print(res)
if __name__=="__main__":
    main()