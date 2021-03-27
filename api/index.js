const express = require('express');
const morgan = require('morgan');
const cors = require('cors');
const helmet = require('helmet');
const monk = require('monk');
require('dotenv').config();

const app = express();

app.use(cors());
app.use(morgan('tiny'));
app.use(helmet());
app.use(express.json());

const url = process.env.MONGO_URI;

const db = monk(url);

db.then(() => {
  console.log('Connected to mongo');
});

const villagers = db.get('villagers');
const fish = db.get('villagers');
const crops = db.get('villagers');
const craftables = db.get('villagers');
const foragables = db.get('villagers');
const animalProducts = db.get('animal_products');
const artisanGoods = db.get('artisan_goods');
const bundles = db.get('bundles');

app.get('/', (req, res) => {
  res.json({
    message: 'Hello world!',
  });
});

app.get('/villagers', (req, res) => {
  villagers.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/villagers/:name', (req, res) => {
  villagers.findOne({ id: req.params.name.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/fish', (req, res) => {
  fish.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/fish/:name', (req, res) => {
  fish.findOne({ id: req.params.name.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/crops', (req, res) => {
  crops.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/crops/:name', (req, res) => {
  crops.findOne({ id: req.params.name.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/craftables', (req, res) => {
  craftables.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/craftables/:name', (req, res) => {
  craftables.findOne({ id: req.params.name.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/foragables', (req, res) => {
  foragables.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/foragables/:name', (req, res) => {
  foragables.findOne({ id: req.params.name.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/artisan_goods', (req, res) => {
  artisanGoods.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/artisan_goods/:name', (req, res) => {
  artisanGoods.findOne({ id: req.params.name.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/animal_products', (req, res) => {
  animalProducts.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/animal_products/:name', (req, res) => {
  animalProducts.findOne({ id: req.params.name.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/bundles', (req, res) => {
  bundles.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

app.get('/bundles/:room', (req, res) => {
  bundles.findOne({ id: req.params.room.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

const port = process.env.PORT || 5000;
app.listen(port, () => {
  console.log(`Listening at http://localhost:${port}`);
});
