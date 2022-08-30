const BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline";
const API_KEY = "ZX7VPUYV36DXTCEP46UQJ6JD6";



async function showInitialForecast() {
    const response = await axios.get(`${BASE_URL}/London,UK/today?unitGroup=us&key=ZX7VPUYV36DXTCEP46UQJ6JD6&include=current&elements=datetime,
                                    description,feelslike,conditions,humidity,precip,preciptype,pressure,snow,snowdepth,sunrise,sunset,
                                    temp,tempmax,tempmin,uvindex,visibility,windspeed,severerisk`);

    console.log("RESPONSE DATA", response.data);     
    console.log("RESPONSE DATA DAYS", response.data.days);                          
    //console.log("CURRENT CONDITIONS", response.data.currentConditions);

    
}

async function showSevenDays(){


    const response2 = await axios.get(`${BASE_URL}/London,UK/next7days?unitGroup=us&key=ZX7VPUYV36DXTCEP46UQJ6JD6&include=current&elements=datetime,
                                    description,feelslike,conditions,humidity,precip,preciptype,pressure,snow,snowdepth,sunrise,sunset,
                                    temp,tempmax,tempmin,uvindex,visibility,windspeed,severerisk`);
    

    let currentConditions = response2.data.currentConditions;
    //console.log(response2.data.days);
    let tests = response2.data.days.map(result => {
        //console.log(result);
         return {
            datetime: result.datetime,
            
            feelslike: result.feelslike,
            conditions: result.conditions,
            humidity: result.humidity,
            precip: result.precip,
            preciptype: result.preciptype,
        };

    }) ;
    console.log(tests);
    
}

/*
pressure,snow,snowdepth,sunrise,sunset,
                                    temp,tempmax,tempmin,uvindex,visibility,windspeed,severerisk */


async function showHours(){


    const response2 = await axios.get(`${BASE_URL}/London,UK/today?unitGroup=us&key=ZX7VPUYV36DXTCEP46UQJ6JD6&include=days,hours,current&elements=datetime,
                                                description,feelslike,conditions,humidity,precip,preciptype,pressure,snow,snowdepth,sunrise,sunset,
                                                        temp,tempmax,tempmin,uvindex,visibility,windspeed,severerisk`);


    console.log(response2.data.days);


    let hours = response2.data.days.map(result => {
        return result.hours;
    
        });
    console.log(hours[0]);
   
    }
    //console.log(hours);
