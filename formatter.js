const fs = require("fs");
const data = JSON.parse(fs.readFileSync("./data.json", "utf-8"));

function convertToAverageTemp(data) {
  const formattedData = {
    oldestYear: Infinity,
    newestYear: -Infinity
  };
  const hokkaidoAggregate = {};

  for (let [pref, prefData] of Object.entries(data)) {
    const aggregatedData = {};

    for (let cityData of Object.values(prefData)) {
      for (let [year, temp] of Object.entries(cityData)) {
        if (+year < formattedData.oldestYear) {
          formattedData.oldestYear = +year;
        }
        if (+year > formattedData.newestYear) {
          formattedData.newestYear = +year;
        }

        if (pref.match("方")) {
          hokkaidoAggregate[year]
            ? hokkaidoAggregate[year].push(temp)
            : (hokkaidoAggregate[year] = [temp]);
        } else {
          aggregatedData[year]
            ? aggregatedData[year].push(temp)
            : (aggregatedData[year] = [temp]);
        }
      }
    }

    // Skips Hokkaido subprefectures and the South Pole
    if (pref.match(/方|南極/)) continue;

    const averagePrefTemps = {};
    for (let [year, yearData] of Object.entries(aggregatedData)) {
      averagePrefTemps[year] = averageArrayValuesInMatrix(yearData);
    }

    formattedData[pref] = averagePrefTemps;
  }

  const averageHokkaidoTemps = {};
  for (let [year, yearData] of Object.entries(hokkaidoAggregate)) {
    averageHokkaidoTemps[year] = averageArrayValuesInMatrix(yearData);
  }
  formattedData["北海道"] = averageHokkaidoTemps;

  return formattedData;
}

function averageArrayValuesInMatrix(matrix) {
  const averageArray = [];

  for (let i = 0; i < matrix[0].length; i++) {
    let sum = 0;
    let count = 0;

    for (let j = 0; j < matrix.length; j++) {
      if (matrix[j][i] !== "") {
        sum += +matrix[j][i];
        count += 1;
      }
    }
    const average = count > 0 ? sum / count : null;
    averageArray.push(average);
  }

  return averageArray;
}

const formattedJSON = JSON.stringify(convertToAverageTemp(data), null, 4);
fs.writeFileSync("formatted.json", formattedJSON);
