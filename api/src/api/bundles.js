const router = require('express').Router();
const db = require('../database');

const bundles = db.get('bundles');

router.get('/', (req, res) => {
  bundles.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

router.get('/:room', (req, res) => {
  bundles.findOne({ id: req.params.room.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

module.exports = router;
