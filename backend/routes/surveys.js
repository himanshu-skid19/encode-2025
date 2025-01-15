const express = require('express');
const router = express.Router();
const Survey = require('../models/Survey');

// Get all surveys
router.get('/', async (req, res) => {
  try {
    const surveys = await Survey.find();
    res.json(surveys);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Create survey
router.post('/', async (req, res) => {
  const survey = new Survey({
    customer_info: req.body.customer_info,
    satisfaction_ratings: req.body.satisfaction_ratings,
    resolution: req.body.resolution,
    detailed_feedback: req.body.detailed_feedback
  });

  try {
    const newSurvey = await survey.save();
    res.status(201).json(newSurvey);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Get survey by ID
router.get('/:id', async (req, res) => {
  try {
    const survey = await Survey.findById(req.params.id);
    if (!survey) {
      return res.status(404).json({ message: 'Survey not found' });
    }
    res.json(survey);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Update survey
router.patch('/:id', async (req, res) => {
  try {
    const survey = await Survey.findById(req.params.id);
    if (!survey) {
      return res.status(404).json({ message: 'Survey not found' });
    }

    Object.keys(req.body).forEach(key => {
      if (req.body[key] !== undefined) {
        survey[key] = req.body[key];
      }
    });

    const updatedSurvey = await survey.save();
    res.json(updatedSurvey);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

module.exports = router;