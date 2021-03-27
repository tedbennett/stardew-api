const router = require('express').Router();
const db = require('../database');

const animalProducts = db.get('animal_products');

router.get('/', (req, res) => {
  animalProducts.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

router.get('/:name', (req, res) => {
  animalProducts.findOne({ id: req.params.name.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

module.exports = router;
