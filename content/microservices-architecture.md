Title: Microservices Architecture: When to Break Your Monolith
Date: 2025-06-23 14:45
Tags: microservices, architecture, backend, scalability, design
Author: Suhail
Summary: A pragmatic guide to microservices architecture, covering when to adopt it, common pitfalls, and lessons learned from real-world implementations.

Microservices aren't a silver bullet. Here's when they make sense and how to avoid the most common mistakes I've seen teams make.

## The Monolith vs Microservices Spectrum

### Starting with a Monolith
```
┌─────────────────────────────────┐
│         Monolithic App          │
├─────────────────────────────────┤
│ User Service    │ Order Service │
│ Product Service │ Payment API   │
│ Notification    │ Analytics     │
└─────────────────────────────────┘
         Single Database
```

**Benefits:**
- Simple deployment and testing
- Easy local development
- Consistent data transactions
- Lower operational complexity

### Breaking into Services
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ User Service│  │Order Service│  │Payment API  │
│     DB      │  │     DB      │  │     DB      │
└─────────────┘  └─────────────┘  └─────────────┘
       │                │                │
       └────────── API Gateway ──────────┘
```

**Benefits:**
- Independent scaling and deployment
- Technology diversity
- Team autonomy
- Fault isolation

## When to Consider Microservices

### Team Size and Organization
```javascript
// Conway's Law in action
const teamStructure = {
  small: "1-8 developers → Monolith",
  medium: "8-25 developers → Modular monolith", 
  large: "25+ developers → Microservices"
};

// Real example: Scaling indicators
const scalingSignals = {
  deploymentFrequency: "Multiple teams waiting for deploy windows",
  developmentSpeed: "Feature development slowing due to conflicts",
  teamAutonomy: "Teams stepping on each other's code",
  technicalRequirements: "Different services need different tech stacks"
};
```

### Business Domain Boundaries
```javascript
// Good service boundaries follow business domains
const ecommerceServices = {
  userManagement: {
    responsibilities: ['authentication', 'profiles', 'preferences'],
    data: ['users', 'sessions', 'permissions']
  },
  
  catalog: {
    responsibilities: ['products', 'inventory', 'search'],
    data: ['products', 'categories', 'stock_levels']
  },
  
  orders: {
    responsibilities: ['cart', 'checkout', 'fulfillment'],
    data: ['orders', 'order_items', 'shipping']
  },
  
  payments: {
    responsibilities: ['billing', 'transactions', 'refunds'],
    data: ['payments', 'invoices', 'payment_methods']
  }
};
```

## Common Microservices Patterns

### API Gateway Pattern
```javascript
// Central entry point for all client requests
const apiGateway = {
  responsibilities: [
    'Request routing',
    'Authentication/Authorization',
    'Rate limiting',
    'Request/Response transformation',
    'Monitoring and logging'
  ],
  
  routes: {
    '/api/users/*': 'user-service:3001',
    '/api/products/*': 'catalog-service:3002',
    '/api/orders/*': 'order-service:3003',
    '/api/payments/*': 'payment-service:3004'
  }
};

// Example implementation with Express
app.use('/api/users', proxy('http://user-service:3001'));
app.use('/api/products', proxy('http://catalog-service:3002'));
```

### Service Discovery
```javascript
// Service registry for dynamic service location
class ServiceRegistry {
  constructor() {
    this.services = new Map();
  }
  
  register(serviceName, serviceInfo) {
    this.services.set(serviceName, {
      ...serviceInfo,
      lastHeartbeat: Date.now()
    });
  }
  
  discover(serviceName) {
    const service = this.services.get(serviceName);
    if (!service) {
      throw new Error(`Service ${serviceName} not found`);
    }
    
    // Check if service is healthy (heartbeat within last 30 seconds)
    if (Date.now() - service.lastHeartbeat > 30000) {
      this.services.delete(serviceName);
      throw new Error(`Service ${serviceName} is unhealthy`);
    }
    
    return service;
  }
}
```

### Circuit Breaker Pattern
```javascript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.threshold = threshold;
    this.timeout = timeout;
    this.failureCount = 0;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.nextAttempt = Date.now();
  }
  
  async call(serviceCall) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit breaker is OPEN');
      }
      this.state = 'HALF_OPEN';
    }
    
    try {
      const result = await serviceCall();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }
  
  onFailure() {
    this.failureCount++;
    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.timeout;
    }
  }
}

// Usage
const paymentServiceBreaker = new CircuitBreaker(3, 30000);

async function processPayment(paymentData) {
  try {
    return await paymentServiceBreaker.call(
      () => paymentService.charge(paymentData)
    );
  } catch (error) {
    // Fallback: queue for later processing
    return await queuePaymentForRetry(paymentData);
  }
}
```

## Data Management Strategies

### Database per Service
```sql
-- User Service Database
CREATE DATABASE user_service;
USE user_service;
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  created_at TIMESTAMP
);

-- Order Service Database  
CREATE DATABASE order_service;
USE order_service;
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  user_id UUID, -- Reference to user service
  total_amount DECIMAL(10,2),
  created_at TIMESTAMP
);
```

### Event-Driven Data Synchronization
```javascript
// When user is created, publish event
class UserService {
  async createUser(userData) {
    const user = await this.database.users.create(userData);
    
    // Publish event for other services
    await this.eventBus.publish('user.created', {
      userId: user.id,
      email: user.email,
      createdAt: user.createdAt
    });
    
    return user;
  }
}

// Other services listen for user events
class OrderService {
  constructor() {
    this.eventBus.subscribe('user.created', this.handleUserCreated.bind(this));
    this.eventBus.subscribe('user.updated', this.handleUserUpdated.bind(this));
  }
  
  async handleUserCreated(event) {
    // Create local user reference for orders
    await this.database.user_references.create({
      userId: event.userId,
      email: event.email
    });
  }
}
```

### Saga Pattern for Distributed Transactions
```javascript
// Choreography-based saga for order processing
class OrderSaga {
  async processOrder(orderData) {
    const sagaId = generateUUID();
    
    try {
      // Step 1: Reserve inventory
      const reservation = await this.inventoryService.reserve(
        orderData.items, sagaId
      );
      
      // Step 2: Process payment
      const payment = await this.paymentService.charge(
        orderData.payment, sagaId
      );
      
      // Step 3: Create order
      const order = await this.orderService.create(
        orderData, sagaId
      );
      
      return order;
      
    } catch (error) {
      // Compensate for any completed steps
      await this.compensate(sagaId, error);
      throw error;
    }
  }
  
  async compensate(sagaId, error) {
    // Rollback in reverse order
    await this.orderService.cancel(sagaId);
    await this.paymentService.refund(sagaId);
    await this.inventoryService.release(sagaId);
  }
}
```

## Communication Patterns

### Synchronous Communication
```javascript
// REST API calls between services
class OrderService {
  async createOrder(orderData) {
    // Validate user exists
    const user = await this.userService.getUser(orderData.userId);
    if (!user) {
      throw new Error('User not found');
    }
    
    // Check inventory
    const availability = await this.inventoryService.checkStock(
      orderData.items
    );
    if (!availability.available) {
      throw new Error('Insufficient stock');
    }
    
    // Process payment
    const payment = await this.paymentService.charge(
      orderData.payment
    );
    
    // Create order
    return await this.database.orders.create({
      ...orderData,
      paymentId: payment.id,
      status: 'confirmed'
    });
  }
}
```

### Asynchronous Communication
```javascript
// Event-driven communication
class EventBus {
  constructor() {
    this.subscribers = new Map();
  }
  
  subscribe(eventType, handler) {
    if (!this.subscribers.has(eventType)) {
      this.subscribers.set(eventType, []);
    }
    this.subscribers.get(eventType).push(handler);
  }
  
  async publish(eventType, eventData) {
    const handlers = this.subscribers.get(eventType) || [];
    
    // Process handlers in parallel
    await Promise.all(
      handlers.map(handler => 
        this.safeExecute(handler, eventData)
      )
    );
  }
  
  async safeExecute(handler, eventData) {
    try {
      await handler(eventData);
    } catch (error) {
      console.error('Event handler failed:', error);
      // Optionally retry or dead letter queue
    }
  }
}
```

## Deployment and Operations

### Container Orchestration
```yaml
# docker-compose.yml for local development
version: '3.8'
services:
  api-gateway:
    build: ./api-gateway
    ports:
      - "3000:3000"
    environment:
      - USER_SERVICE_URL=http://user-service:3001
      - ORDER_SERVICE_URL=http://order-service:3002
    depends_on:
      - user-service
      - order-service
  
  user-service:
    build: ./user-service
    ports:
      - "3001:3000"
    environment:
      - DATABASE_URL=postgres://user:pass@user-db:5432/users
    depends_on:
      - user-db
  
  order-service:
    build: ./order-service
    ports:
      - "3002:3000"
    environment:
      - DATABASE_URL=postgres://order:pass@order-db:5432/orders
    depends_on:
      - order-db
```

### Kubernetes Deployment
```yaml
# user-service-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: user-service
        image: user-service:latest
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: user-db-secret
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
  - port: 80
    targetPort: 3000
  type: ClusterIP
```

## Monitoring and Observability

### Distributed Tracing
```javascript
const opentelemetry = require('@opentelemetry/api');
const tracer = opentelemetry.trace.getTracer('order-service');

async function processOrder(orderData) {
  const span = tracer.startSpan('process_order');
  span.setAttributes({
    'order.id': orderData.id,
    'order.amount': orderData.total,
    'user.id': orderData.userId
  });
  
  try {
    // Child span for user validation
    const userSpan = tracer.startSpan('validate_user', { parent: span });
    const user = await validateUser(orderData.userId);
    userSpan.end();
    
    // Child span for payment processing
    const paymentSpan = tracer.startSpan('process_payment', { parent: span });
    const payment = await processPayment(orderData.payment);
    paymentSpan.end();
    
    span.setStatus({ code: opentelemetry.SpanStatusCode.OK });
    return { orderId: generateOrderId(), paymentId: payment.id };
    
  } catch (error) {
    span.recordException(error);
    span.setStatus({ 
      code: opentelemetry.SpanStatusCode.ERROR,
      message: error.message 
    });
    throw error;
  } finally {
    span.end();
  }
}
```

### Health Checks
```javascript
// Health check endpoint for each service
app.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'user-service',
    version: process.env.SERVICE_VERSION,
    dependencies: {}
  };
  
  try {
    // Check database connection
    await database.query('SELECT 1');
    health.dependencies.database = 'healthy';
  } catch (error) {
    health.dependencies.database = 'unhealthy';
    health.status = 'degraded';
  }
  
  try {
    // Check external service dependencies
    await externalApi.ping();
    health.dependencies.externalApi = 'healthy';
  } catch (error) {
    health.dependencies.externalApi = 'unhealthy';
    health.status = 'degraded';
  }
  
  const statusCode = health.status === 'healthy' ? 200 : 503;
  res.status(statusCode).json(health);
});
```

## Common Pitfalls and Solutions

### 1. Distributed Monolith
**Problem**: Services too tightly coupled
```javascript
// Anti-pattern: Synchronous calls creating dependency chains
async function getUserOrders(userId) {
  const user = await userService.getUser(userId); // Call 1
  const orders = await orderService.getOrdersByUser(userId); // Call 2
  
  for (let order of orders) {
    order.items = await catalogService.getItems(order.itemIds); // Call 3+
    order.payment = await paymentService.getPayment(order.paymentId); // Call 4+
  }
  
  return { user, orders };
}
```

**Solution**: Event-driven architecture with data denormalization
```javascript
// Better: Precomputed views with eventual consistency
class OrderViewService {
  async getUserOrderView(userId) {
    // Single query returns denormalized data
    return await this.database.userOrderViews.findByUserId(userId);
  }
  
  // Updated via events from other services
  async handleOrderCreated(event) {
    await this.updateUserOrderView(event.userId, event.orderData);
  }
}
```

### 2. Data Consistency Issues
**Problem**: Eventual consistency causing user confusion
**Solution**: Implement proper event sourcing and CQRS patterns

### 3. Network Latency
**Problem**: Too many service calls for single operations
**Solution**: Batch operations, caching, and async processing

## Decision Framework

### Questions to Ask Before Adopting Microservices
1. **Team size**: Do we have enough developers to maintain multiple services?
2. **Domain complexity**: Are there clear bounded contexts?
3. **Scalability needs**: Do different parts need different scaling strategies?
4. **Deployment frequency**: Do we need independent deployment cycles?
5. **Technology diversity**: Do we need different tech stacks?
6. **Operational maturity**: Can we handle distributed system complexity?

### Migration Strategy
```javascript
// Phase 1: Extract first service (least dependent)
const migrationPlan = {
  phase1: 'Extract notification service (few dependencies)',
  phase2: 'Extract user service (well-defined boundary)',
  phase3: 'Extract catalog service (read-heavy, cacheable)',
  phase4: 'Extract order service (complex but valuable)',
  phase5: 'Extract payment service (security requirements)'
};
```

Remember: Microservices are about solving organizational and scaling problems, not technical ones. Start with a monolith, understand your domain boundaries, and extract services when the benefits clearly outweigh the added complexity.