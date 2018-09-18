# RaspberryPi-IoT-to-AWS
Used to import data using BNO055 sensor and dropping data into AWS S3 bucket.

This does not have that strong of secuirty... none. Once into AWS' cloud however, the secuirty is strong. Just keys cannot be shared.

User will need to uncomment what specific methods that they want the sensor to pull data off of.
And user will need to give personal keys and bucket name for it to drop CSV files onto their specified bucket.

In production, the user will hide the keys using the "client" strategy putting the file onto the root of the file directory in a hidden folder.
