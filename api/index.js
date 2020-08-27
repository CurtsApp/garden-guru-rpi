const express = require('express')
const fs = require('fs');
const os = require('os');
const app = express()
const port = 3000

app.get('/', (req, res) => {
    const description = {
        name: "Gidget",
        purpose: "Record tempurature and humidity data"
    }
    res.send(JSON.stringify(description))
})

app.get('/data', (req, res) => {


    const startDT = new Date(parseInt(req.query.sDateTime));
    const endDT = new Date(parseInt(req.query.eDateTime));

    if (isNaN(startDT.getTime()) || isNaN(endDT.getTime())) {
        res.status(400).send("Malformed start or end date-time");
    } else {
        console.log("Start Date: " + startDT);
        console.log("End Date: " + endDT);

        getDateDataInRange(startDT, endDT).then((fulfilled) => {

            const description = {
                data: fulfilled
            }
            res.send(JSON.stringify(description));
        }).catch((rej) => {
            res.send(JSON.stringify({error: rej}));
        });
    }


});

function getMonthDays(month, year) {
    if (month < 0 || month > 12) {
        throw new Error("What are you doing?");
    } else {
        return new Date(year, month, 0).getDate();
    }
}

function getDateDataInRange(sDate, eDate) {
    let getDatePromises = [];
    let inspectDate = new Date(sDate);
    inspectDate.setHours(0,0,0,0);
    while (inspectDate < eDate) {
        //console.log("Getting... " + JSON.stringify((inspectDate)));
        getDatePromises.push(getDateData(inspectDate));
        inspectDate.setDate(inspectDate.getDate() + 1);
    }
    return new Promise((resolve, reject) => {
        Promise.all(getDatePromises).then((res) => {
            /*
            res should be an array of, arrays of day data

            Chop out unincluded times of first and last days
             */
            const daysTimePoints = res;
            console.log(res);
            let firstDayTimePoints = daysTimePoints[0];
            // Remove time points before start time
            daysTimePoints[0] = firstDayTimePoints.filter(timePoint => {
                return timePoint.time.getTime() < sDate.getTime();
            });
            let lastDayTimePoints = daysTimePoints[daysTimePoints.length - 1];
            // Remove time points after end time
            daysTimePoints[daysTimePoints.length - 1] = lastDayTimePoints.filter(timePoint => {
                return timePoint.time.getTime() > eDate.getTime();
            });

            resolve([].concat.apply([], daysTimePoints));
        });
    });
}

/*
date =
{
year,
month,
day
 */

function getDateData(date) {
    return new Promise((resolve, reject) => {

        const fileName = `${formatDateNum(date.getDate())}-${formatDateNum(date.getMonth() + 1)}-${date.getFullYear()}.log`;
        const logPath = getLogPath();
        const filePath = `${logPath}/${fileName}`;
        console.log("Getting... " + filePath);
        fs.readFile(filePath, "utf8", function (err, data) {
            const timePoints = [];
            if (data) {
                /*
                {date-time,
                temp,
                humidity}
                */
                // Last row has extra new line character
                const timeRows = data.split("\n").filter(row => {
                    return row !== "";
                });
                for (const row of timeRows) {
                    const splitRow = row.split(",");
                    const timePieces = splitRow[0].split(":");
                    const time = new Date(0);
                    time.setHours(parseInt(timePieces[0]), parseInt(timePieces[1]), parseInt(timePieces[2]));
                    time.setFullYear(date.getFullYear(), date.getMonth(), date.getDate());
                    timePoints.push({
                        time: time,
                        temp: parseInt(splitRow[1]),
                        humidity: parseFloat(splitRow[2])
                    })
                }
            }
            resolve(timePoints);
        });
    });
}

function formatDateNum(num) {
    if (num < 10) {
        return "0" + num.toString();
    } else {
        return num.toString()
    }
}

function getLogPath() {
    if (isLinux()) {
        return "/home/pi/code/log/temp"
    } else {
        return "./../src/log/temp"
    }
}

function isLinux() {
    return os.platform === "Linux"
}

app.listen(port, () => {
    console.log(`Gidget is listening at http://localhost:${port}`);
})