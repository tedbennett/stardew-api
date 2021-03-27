const router = require('express').Router();
const db = require('../database');

const artisanGoods = db.get('artisan_goods');

router.get('/', (req, res) => {
  artisanGoods.find()
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

router.get('/:name', (req, res) => {
  artisanGoods.findOne({ id: req.params.name.toLowerCase() })
    .then((docs) => {
      res.json({
        data: docs,
      });
    });
});

module.exports = router;
