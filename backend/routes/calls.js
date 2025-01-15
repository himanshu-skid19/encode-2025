const express = require('express');
const router = express.Router();
const Call = require('../models/Call');

// Get all calls
router.get('/', async (req, res) => {
  try {
    const calls = await Call.find();
    res.json(calls);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Get calls by customer ID
router.get('/customer/:customerId', async (req, res) => {
  try {
    const calls = await Call.find({ customer_id: parseInt(req.params.customerId) });
    res.json(calls);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Create call
router.post('/', async (req, res) => {
  const call = new Call({
    transcribed_call: req.body.transcribed_call,
    score: req.body.score,
    customer_id: req.body.customer_id
  });

  try {
    const newCall = await call.save();
    res.status(201).json(newCall);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Update call
router.patch('/:id', async (req, res) => {
  try {
    const call = await Call.findById(req.params.id);
    if (!call) {
      return res.status(404).json({ message: 'Call not found' });
    }

    if (req.body.transcribed_call) call.transcribed_call = req.body.transcribed_call;
    if (req.body.score !== undefined) call.score = req.body.score;
    if (req.body.customer_id) call.customer_id = req.body.customer_id;

    const updatedCall = await call.save();
    res.json(updatedCall);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

module.exports = router;