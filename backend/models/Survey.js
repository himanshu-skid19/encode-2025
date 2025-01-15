const mongoose = require('mongoose');

const SurveySchema = new mongoose.Schema({
  customer_info: {
    name: String,
    email: String,
    contact_number: String
  },
  satisfaction_ratings: {
    overall: Number,
    response_time: String
  },
  resolution: {
    issue_resolved: String,
    pending_issues: String
  },
  detailed_feedback: {
    strengths: [String],
    improvements: [String],
    additional_comments: String
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Survey', SurveySchema);