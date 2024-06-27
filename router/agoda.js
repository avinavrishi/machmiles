
const express = require('express');
const axios = require('axios');

const router = express.Router();

router.get('/autocomplete', async (req, res) => {
const { query } = req.query;

const options = {
    method: 'GET',
    url: 'https://agoda-com.p.rapidapi.com/flights/auto-complete',
    params: { query: query },
    headers: {
    'x-rapidapi-key': process.env.RAPIDAPI_KEY,
    'x-rapidapi-host': process.env.RAPIDAPI_HOST
    }
};

try {
    const response = await axios.request(options);
    const suggestions = [];

    response.data.data.forEach(item => {

    // Add each airport in the item's airports list
    if (item.airports && item.airports.length > 0) {
        item.airports.forEach(airport => {
        suggestions.push({
            name: airport.name,
            code: airport.code
        });
        });
    }

    });

    res.json(suggestions);
} catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
}
});

router.get('/search-flights', async (req, res) => {
const { flying_from, flying_to, departure_date, adults, children, infants, return_date } = req.query;

const options = {
    method: 'GET',
    url: 'https://agoda-com.p.rapidapi.com/flights/search-one-way',
    params: {
        origin: flying_from,
        destination: flying_to,
        departureDate: departure_date,
        adults: adults,
        children: children,
        infants: infants
    },
    headers: {
        'x-rapidapi-key': process.env.RAPIDAPI_KEY,
        'x-rapidapi-host': process.env.RAPIDAPI_HOST
    }
};

try {
    const response = await axios.request(options);
    const bundles = response.data.data.bundles || [];

    // console.log(response.data.data);
    // console.log("==================")
    // Log keys of each bundle object
    // bundles.forEach((bundle, index) => {
    //     console.log(`Bundle ${index + 1} keys:`);
    //     console.log(Object.keys(bundle));
    // });

    res.render('pages/results', { bundles });
} catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
}
});

router.get('/flight-details', async (req, res) => {
const { id, token } = req.query;

const options = {
    method: 'GET',
    url: 'https://agoda-com.p.rapidapi.com/flights/details',
    params: {
        itineraryId : id,
        token : token
    },
    headers: {
        'x-rapidapi-key': process.env.RAPIDAPI_KEY,
        'x-rapidapi-host': process.env.RAPIDAPI_HOST
    }
};

try {
    const response = await axios.request(options);
    const bundles = response.data.data.bundles || [];

    data = response.data;

    console.log(response.data);
    console.log("==================");

    res.render('pages/flight_data', { data });

} catch (error) {

    console.error(error);
    res.status(500).json({ error: error.message });
}
});

router.get('/all-language', async (req, res) => {
const { id, token } = req.query;

const options = {
    method: 'GET',
    url: 'https://agoda-com.p.rapidapi.com/languages',
    headers: {
    'x-rapidapi-key': 'f419aee40cmsh30d7ffb65a062fbp145396jsn95b5295dfb39',
    'x-rapidapi-host': 'agoda-com.p.rapidapi.com'
    }
};

try {
    const response = await axios.request(options);
    console.log(response.data);
} catch (error) {
    console.error(error);
}

});

router.get('/all-language', async (req, res) => {

    const options = {
    method: 'GET',
    url: 'https://agoda-com.p.rapidapi.com/currencies',
    headers: {
        'x-rapidapi-key': 'f419aee40cmsh30d7ffb65a062fbp145396jsn95b5295dfb39',
        'x-rapidapi-host': 'agoda-com.p.rapidapi.com'
    }
    };

    try {
    const response = await axios.request(options);
    console.log(response.data);
    } catch (error) {
    console.error(error);
    }

});

module.exports = router;
