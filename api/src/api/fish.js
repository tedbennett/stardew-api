const router = require('express').Router();
const db = require('../database');

const fish = db.get('fish');

router.get('/', (req, res) => {
  fish.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

router.get('/:name', (req, res) => {
  fish.findOne({ id: req.params.name.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

module.exports = router;
