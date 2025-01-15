const mongoose = require('mongoose');

const CustomerSchema = new mongoose.Schema({
  customer_number: {
    type: Number,
    required: true,
    unique: true
  },
  name: {
    type: String,
    required: true
  },
  products: [{
    product_id: Number,
    date_bought: Date
  }],
  customer_id: {
    type: Number,
    required: true,
    unique: true
  },
  customer_score: {
    type: Number,
    default: 0
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Customer', CustomerSchema);