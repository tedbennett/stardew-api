const express = require('express');

const morgan = require('morgan');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

const animalProducts = require('./api/animal-products');
const artisanGoods = require('./api/artisan-goods');
const bundles = require('./api/bundles');
const craftables = require('./api/craftables');
const crops = require('./api/crops');
const fish = require('./api/fish');
const foragables = require('./api/foragables');
const villagers = require('./api/villagers');

const app = express();

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 2000,
});

app.use(cors());
app.use(morgan('tiny'));
app.use(helmet());
app.use(express.json());
app.use(limiter);

app.get('/', (req, res) => {
  res.json({
    message: 'Hello world!',
  });
});

app.use('/crops', crops);
app.use('/animalProducts', animalProducts);
app.use('/artisanGoods', artisanGoods);
app.use('/bundles', bundles);
app.use('/craftables', craftables);
app.use('/crops', crops);
app.use('/fish', fish);
app.use('/foragables', foragables);
app.use('/villagers', villagers);

module.exports = app;
