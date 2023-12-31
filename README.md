# External API Project 
Welcome to the documentation for External API Project, which consists of multiple apps. Below, you'll find details on each app's API.

## Random Image API
This API allows you to retrieve a random image from a predefined directory and to post image-related data.

### Retrieve a Random Image

### Endpoint

- **GET** `/image/`

### Usage

To retrieve a random image, make a GET request to the `/image/` endpoint.

## Pickup API
The `getPickup/getRandomRizz` API allows you to retrieve a random pickup line from the database and return a random pickup line to the user.

### Retrieve a Random Pickup Line

- **GET** `/getPickup/getRandomRizz/`

#### Response

The response will be a plain text string containing a random pickup line. 

##### Example
"My favorite element on the periodic table is Uranium, because I am in love with U."

- **GET** `/getPickup/getMostViewedLine/`

#### Response

The response will return the most viewed pickup line for each device, mentioning the device ID and the respective pickup line.

##### Example
```json
[
    {
        "device_id": "2d4d9f1868ed11ee8c990242ac120002",
        "pickup_line": "My favorite element on the periodic table is Uranium, because I am in love with U."
    },
    {
        "device_id": "6d9b85045eed424eaf2efbc96cd8e9a3",
        "pickup_line": "Are you a camera? Because every time I see you I smile"
    },
    {
        "device_id": "6d9b85045eed424eaf2efbc96cd8e9a9",
        "pickup_line": "Are you cryptocurrency? Coz I wanna hold you for so long."
    },
    {
        "device_id": "6d9b85045eed424eaf2efbc96cd8e9c3",
        "pickup_line": "Was your father a thief? Because someone stole the stars from the sky and put them in your eyes."
    },
]
```

- **GET** `/getPickup/getMostViewedAll/`

#### Response

The response will be a plain text string that contains the most viewed pickup line across all devices.

##### Example
"The most viewed pickup line by all devices is 'Are you cryptocurrency? Coz I wanna hold you for so long.' with a count of 5."

## NASA API

The `getNASA` API allows you to retrieve NASA's Astronomy Picture of the Day (APOD) for a specific date.

### Retrieve NASA APOD for a Date

- **GET** `/getNASA?date`

#### Parameters

- `date` (required): The date for which you want to retrieve the APOD image. It should be in the format `YYYY-MM-DD`.

#### Response

The response will be a JSON object containing data specific to the requested date.

##### Example
```json
{
    "id": 7607,
    "date": "2000-03-06",
    "explanation": "Over the course of billions of years, whole clusters of galaxies merge.  Above is an X-ray image of Abell 2142, the result of the collision of two huge clusters of galaxies, and one of the most massive objects known in the universe.  This false-color image shows a concentration of gas 50 million degrees hot near the center of the resulting cluster.  Oddly, it is the relative coldness of the gas that makes this situation particularly interesting.  The center of Abell 2142 is surrounded by gas fully twice as hot, a temperature thought to have been created by energy released during the colossal collision.  Still, since we can only see a snapshot in time, much remains unknown about how clusters of galaxies form and coalesce.",
    "hdurl": "https://apod.nasa.gov/apod/image/0003/abell2142_chandra_big.jpg",
    "media_type": "image",
    "service_version": "v1",
    "title": "Abell 2142: Clash of the Galaxy Clusters",
    "url": "https://apod.nasa.gov/apod/image/0003/abell2142_chandra.jpg",
    "hd_image": null,
    "standard_image": null
}
```

## Speed Test API

The `speed_test` API allows you to perform a network speed test and record the results, including the speed, date and time of the test, binary URL, device information, and system version.

### Perform a Network Speed Test

- **POST** `/speed_test/`

#### Request Body

- `Speed` (required): The network speed in Mbps.
- `DateTime` (required): The date and time of the speed test in the format `YYYY-MM-DD HH:MM:SS.SSSSSS`.
- `BinaryUrl` (required): The binary URL used for the speed test.
- `Device Name Model` (required): The model name of the device used for the speed test.
- `SystemVersion` (required): The system version or OS version of the device.
- `DeviceId` (required): The unique identifier of the device.
- `WidgetFamily` (required): The widget family information.

The `GET` method allows you to retrieve all POST requests made by the user.
- **GET** `/speed_test/`

## TV Show Quotes API

The `getTVQuotes` API allows you to retrieve quotes from various TV shows. It offers different endpoints for fetching quotes with optional parameters like the number of quotes, show name, and short format.

### Retrieve Quotes

- **GET** `/getTVQuotes/quotes`
  
#### Response

This endpoint fetches a random TV show quote from db.

##### Example
```json
{
    "show": "The Middle",
    "character": "Frankie",
    "text": "Frankie: [v.o.] I read something somewhere about: \"No matter how dark the night, the sun comes up... ...and something, something.\" Anyway, the sun came up, and it sure didn't make that room look any better."
}
```

- **GET** `/getTVQuotes/quotes/{number}`

#### Response
   This endpoint fetches a specified number of random TV show quotes. You can customize the number of quotes to retrieve.

##### Example
```json
[
    {
        "show": "Brooklyn Nine-Nine",
        "character": "Hitchcock",
        "text": "Hitchcock: I got it. No! My ass. It left the chair.\nScully: I'm sorry, man.\nHitchcock: No. It was my time."
    },
    {
        "show": "Lucifer",
        "character": "Lucifer Morningstar",
        "text": "Lately I've been thinking. Do you think I'm the Devil because I'm inherently evil, or just because dear ol' dad decided I was?"
    },
    {
        "show": "The Office",
        "character": "Michael Scott",
        "text": "Michael Scott: Cold front coming into the warehouse! Better put on your ski boots! Happy New Year, Darryl. Hey, Darryl. You ever done this?"
    }
]
```

- **GET** `/getTVQuotes/quotes?show={show_name}&short={true/false}`

#### Response
  This endpoint allows you to filter quotes by specifying the TV show name and whether you want short or full quotes.

##### Example
```json
{
    "id": 327,
    "show": "Frasier",
    "character": "Martin",
    "text": "Daphne: I just thought this would be the first child for both of us. You could be a daddy already. There could be dozens of little Niles Cranes running around. He could be your son. Or him.\nNiles: Oh, please, they look nothing like me. Besides, I only went down there one time. It's possible they never used my sample.\n[An extremely handsome blonde-haired man with an incredible physique comes over to the table] \nMan: Can I borrow your sugar?\nDaphne: Yeah.\nNiles: [watching the man walk away] I better look into this.",
    "short": "false"
}
```

- **GET** `/getTVQuotes/quotes/{number}?show={show_name}&short={true/false}`
#### Response
  This endpoint combines the features of specifying the number of quotes, TV show name, and short/full format.
##### Example
```json
[
    {
        "id": 82,
        "show": "Frasier",
        "character": "Niles",
        "text": "Niles: Dad, are you sure you want to do this? I spoke at a career day once. It was a disaster. All the taunting and yelling, I haven't been so... I haven't been so afraid of third graders since ninth grade.",
        "short": "true"
    },
    {
        "id": 77,
        "show": "Frasier",
        "character": "Niles",
        "text": "Niles: Oh, this one's from your mom. A kitten in a basket of yarn. [opens reads the card] \"Dear Niles, I know we haven't always gotten along...\" [checks the other side, but nothing] Wasn't that sweet of her?",
        "short": "true"
    },
    {
        "id": 83,
        "show": "Frasier",
        "character": "Frasier",
        "text": "Frasier: Oh, great. Oh, thank God. By tonight my dad will be safely back in his beer-stained, flea-infested, duct-taped recliner, adjusting his shorts with one hand and cheering on Jean-Claude van Damme with the other. Yes, it's quite a little piece of heaven I've carved out for myself, isn't it?",
        "short": "true"
    },
    {
        "id": 84,
        "show": "Frasier",
        "character": "Niles",
        "text": "Niles: Yes, well. This has been delightful, but I really must run. I'm due at my sexual addiction group, and I don't like to leave them alone for too long.",
        "short": "true"
    }
]
```

## Numbers API
The `factoftheDay/{month_in_number_format}/{day_in_number_format}/date` API allows you to retrieve a fact of the day from the database for a specific date.Please note that while the day and month are fixed, the year is variable and can be any year. This means you can retrieve a fact for the same day and month across different years.
  
### Retrieve a Random Pickup Line

- **GET** `factoftheDay/11/2/date`

#### Response

The response will be a plain text string containing a fact of the day for that date. 

##### Example
"November 2nd is the day in 1930 that Haile Selassie is crowned emperor of Ethiopia."

## Word of the Day API
The `wordOftheDay/` API returns the word of the day for today's date in both Hindi and English, along with usage examples in both languages.
  
### Retrieve a Random Pickup Line

- **GET** `wordOftheDay/`

#### Response

The response will return a JSON response of word of the day data for today's date in both Hindi and English, along with usage examples in both languages. 

##### Example
```json
{
    "id": 43,
    "wordOfTheDayinHindi": "अस्पष्ट",
    "wordOfTheDayinEnglish": "ambiguous",
    "wordOfTheDayinEnglish_Usage_Example": "Everyone listened to the weather report, but the forecast was ambiguous and no one knew if it was going to be rainy or sunny today.",
    "wordOfTheDayinHindi_Usage_Example": "हर किसी ने मौसम के समाचार को सुना था, लेकिन उनका पूर्वानुमान अस्पष्ट था और कोई भी यह नहीं जान पाया कि आज बरसात होगी या धूप खिलेगी।",
    "date": "2023-10-17"
}
```





  















