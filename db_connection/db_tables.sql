CREATE TABLE notifications (
    notification_id UUID PRIMARY KEY,
    notification_type TEXT CHECK (notification_type IN ('SMS', 'EMAIL', 'PUSH')) NOT NULL,
    notification_template TEXT NOT NULL,
    priority TEXT CHECK (priority IN ('high', 'medium', 'low')),
    status TEXT CHECK (status IN ('pending', 'sent', 'failed')) DEFAULT 'pending',
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
)

CREATE TABLE notification_templates (
    id SERIAL PRIMARY KEY,
    template_name TEXT UNIQUE NOT NULL,
    notification_type TEXT CHECK (notification_type IN ('SMS', 'EMAIL', 'PUSH')) NOT NULL,
    language TEXT NOT NULL DEFAULT 'en',
    subject TEXT,
    body TEXT NOT NULL,
    placeholders JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
)

INSERT INTO notification_templates (template_name, notification_type, language, subject, body, placeholders) VALUES 
('USER_REGISTER', 'SMS', 'en', NULL, 'Hi {{user_name}}, welcome to our service!', '{"user_name": "{{user_name}}"}'),
('PAYMENT_SUCCESS', 'SMS', 'en', NULL, 'Hello {{user_name}}, your payment of {{amount}} was successful.','{"user_name": "{{user_name}}", "amount": "{{amount}}"}'),
('ORDER_CONFIRMATION', 'EMAIL', 'en', 'Order Confirmation','Hi {{user_name}}, your order #{{order_id}} has been confirmed.','{"user_name": "{{user_name}}", "order_id": "{{order_id}}"}'),
('OTP', 'SMS', 'en', NULL,'Your OTP is: {{otp}}.', '{"otp": "{{otp}}"}');
