const mongoose = require('mongoose');

const CallSchema = new mongoose.Schema({
  transcribed_call: {
    type: String,
    required: true
  },
  score: {
    type: Number,
    required: true,
    min: 0,
    max: 1
  },
  customer_id: {
    type: Number,
    required: true
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Call', CallSchema);