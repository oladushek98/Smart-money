let parse_data = (row_data) => {
    row_data = row_data.replace(/&quot;/g, '"');
    row_data = JSON.parse(row_data);
    try {
        row_data.forEach((element)=> {element[0] = element[0].replace(/~/g, '"')});
    } catch (err) {
    }
    return row_data
};