const fs = require("fs");
const data = JSON.parse(fs.readFileSync("./data.json", "utf-8"));

function convertToAverageTemp(data) {
  const formattedData = {};

  for (let [pref, prefData] of Object.entries(data)) {
    const aggregatedData = {};

    for (let cityData in prefData) {
      for (let [year, temp] of Object.entries(cityData)) {
        aggregatedData[year]
          ? aggregatedData[year].push(temp)
          : (aggregatedData[year] = [temp]);
      }
    }

    const temps = {};

    for (let [year, yearData] of Object.entries(aggregatedData)) {
      const averageMonthlyTemp = [];

      for (let i = 0; i < yearData[0].length; i++) {
        let sum = 0;
        let count = 0;

        for (let j = 0; j < yearData.length; j++) {
          if (yearData[j][i] !== "") {
            sum += +yearData[j][i];
            count += 1;
          }
        }
        const average = count > 0 ? sum / count : null;
        averageMonthlyTemp.push(average);
      }

      temps[year] = averageMonthlyTemp;
    }

    formattedData[pref] = temps;
  }

  return formattedData;
}

const formattedJSON = JSON.stringify(convertToAverageTemp(data), null, 4);
fs.writeFileSync("formatted.json", formattedJSON);
