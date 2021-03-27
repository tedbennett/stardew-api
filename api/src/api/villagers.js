const router = require('express').Router();
const db = require('../database');

const villagers = db.get('villagers');

router.get('/', (req, res) => {
  villagers.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

router.get('/:name', (req, res) => {
  villagers.findOne({ id: req.params.name.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

module.exports = router;
