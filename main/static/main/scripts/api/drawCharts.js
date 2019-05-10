let parse_data = (row_data) => {
    row_data = row_data.replace(/&quot;/g, '"');
    row_data = JSON.parse(row_data);
    try {
        row_data[1][0] = row_data[1][0].replace(/&#39;/g, '"');
    } catch (err) {
    }
    return row_data
};