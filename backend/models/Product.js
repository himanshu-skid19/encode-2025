const mongoose = require('mongoose');

const ProductSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true
  },
  id: {
    type: String,
    required: true,
    unique: true
  },
  price: {
    type: Number,
    required: true
  },
  type: {
    type: String,
    required: true
  },
  offers: String,
  warranty_details: String,
  description: String
}, {
  timestamps: true
});

module.exports = mongoose.model('Product', ProductSchema);