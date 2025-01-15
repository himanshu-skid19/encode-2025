const express = require('express');
const router = express.Router();
const Customer = require('../models/Customer');

// Get all customers
router.get('/', async (req, res) => {
  try {
    const customers = await Customer.find();
    res.json(customers);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Get one customer by ID
router.get('/:customerId', async (req, res) => {
  try {
    const customer = await Customer.findOne({ customer_id: parseInt(req.params.customerId) });
    if (!customer) {
      return res.status(404).json({ message: 'Customer not found' });
    }
    res.json(customer);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Create customer
router.post('/', async (req, res) => {
  const customer = new Customer({
    customer_number: req.body.customer_number,
    name: req.body.name,
    products: req.body.products,
    customer_id: req.body.customer_id,
    customer_score: req.body.customer_score || 0
  });

  try {
    const newCustomer = await customer.save();
    res.status(201).json(newCustomer);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Update customer
router.patch('/:customerId', async (req, res) => {
  try {
    const customer = await Customer.findOne({ customer_id: parseInt(req.params.customerId) });
    if (!customer) {
      return res.status(404).json({ message: 'Customer not found' });
    }

    if (req.body.customer_number) customer.customer_number = req.body.customer_number;
    if (req.body.name) customer.name = req.body.name;
    if (req.body.products) customer.products = req.body.products;
    if (req.body.customer_score !== undefined) customer.customer_score = req.body.customer_score;

    const updatedCustomer = await customer.save();
    res.json(updatedCustomer);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Delete customer
router.delete('/:customerId', async (req, res) => {
  try {
    const customer = await Customer.findOne({ customer_id: parseInt(req.params.customerId) });
    if (!customer) {
      return res.status(404).json({ message: 'Customer not found' });
    }
    await customer.remove();
    res.json({ message: 'Customer deleted' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

module.exports = router;