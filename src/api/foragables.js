const router = require('express').Router();
const db = require('../database');

const foragables = db.get('foragables');

router.get('/', (req, res) => {
  foragables.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

router.get('/:name', (req, res) => {
  foragables.findOne({ id: req.params.name.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

module.exports = router;
