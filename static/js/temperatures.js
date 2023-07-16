const getSettings = async() => {
    const response = await fetch("/api/settings");
    const jsonData = await response.json();

    return jsonData;
}

const removePseudoTable = async(pseudo_table_id) => {
    const response = await fetch("/api/temperatures/" + pseudo_table_id, {
        method: 'DELETE',
        headers: {
            "Content-Type": "application/json"
        }
    });
    const jsonData = await response.json();
    return jsonData;
}

const setSetting = async(k, v) => {
    const response = await fetch("/api/settings", {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            k: k,
            v: v
        })
    });
    const jsonData = await response.json();

    return jsonData;
}

const getTables = async() => {
    const response = await fetch("/api/pseudo_tables");
    const jsonData = await response.json();

    return jsonData;
}

const getTemperatures = async(pseudo_table_id) => {
    const response = await fetch("/api/temperatures/" + pseudo_table_id);
    const jsonData = await response.json();

    return jsonData;
}