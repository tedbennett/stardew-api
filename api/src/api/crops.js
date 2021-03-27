const router = require('express').Router();
const db = require('../database');

const crops = db.get('crops');

router.get('/', (req, res) => {
  crops.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

router.get('/:name', (req, res) => {
  crops.findOne({ id: req.params.name.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

module.exports = router;
