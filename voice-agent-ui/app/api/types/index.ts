export interface ICustomer {
    customer_number: number;
    name: string;
    products: Array<{
      product_id: number;
      date_bought: Date;
    }>;
    customer_id: number;
    customer_score: number;
    createdAt?: Date;
    updatedAt?: Date;
  }
  
  export interface IProduct {
    name: string;
    id: string;
    price: number;
    type: string;
    offers?: string;
    warranty_details?: string;
    description?: string;
  }
  
  export interface ICall {
    transcribed_call: string;
    score: number;
    customer_id: number;
  }
  
  export interface ISurvey {
    customer_info: {
      name: string;
      email: string;
      contact_number: string;
    };
    satisfaction_ratings: {
      overall: number;
      response_time: string;
    };
    resolution: {
      issue_resolved: string;
      pending_issues: string;
    };
    detailed_feedback: {
      strengths: string[];
      improvements: string[];
      additional_comments: string;
    };
  }
  