const router = require('express').Router();
const db = require('../database');

const craftables = db.get('craftables');

router.get('/', (req, res) => {
  craftables.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

router.get('/:name', (req, res) => {
  craftables.findOne({ id: req.params.name.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

module.exports = router;
