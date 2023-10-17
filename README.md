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

## NASA API

The `getNASA` API allows you to retrieve NASA's Astronomy Picture of the Day (APOD) for a specific date.

### Retrieve NASA APOD for a Date

- **GET** `/getNASA?date`

#### Parameters

- `date` (required): The date for which you want to retrieve the APOD image. It should be in the format `YYYY-MM-DD`.

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
  
  This endpoint fetches a random TV show quote.

- **GET** `/getTVQuotes/quotes/{number}`

  This endpoint fetches a specified number of random TV show quotes. You can customize the number of quotes to retrieve.

- **GET** `/getTVQuotes/quotes?show={show_name}&short={true/false}`

  This endpoint allows you to filter quotes by specifying the TV show name and whether you want short or full quotes.

- **GET** `/getTVQuotes/quotes/{number}?show={show_name}&short={true/false}`

  This endpoint combines the features of specifying the number of quotes, TV show name, and short/full format.

  















