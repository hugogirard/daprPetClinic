using Dapr.Workflow;
using Dapr.Client;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Contoso.Activities;
using Contoso.Models;
using Contoso.Workflows;

var builder = Host.CreateDefaultBuilder(args).ConfigureServices(services =>
{
    services.AddDaprClient();
    services.AddDaprWorkflow(options =>
    {
        options.RegisterWorkflow<ProcessOrder>();
        options.RegisterActivity<ProcessPaymentActivity>();
        options.RegisterActivity<NotifyWarehouseActivity>();
    });
});

var host = await builder.StartAsync();

await using var scope = host.Services.CreateAsyncScope();
var daprWorkflowClient = scope.ServiceProvider.GetRequiredService<DaprWorkflowClient>();
var daprClient = scope.ServiceProvider.GetRequiredService<DaprClient>();

// Example: Retrieve order from Dapr state store
// Replace "statestore" with your actual state store name
// Replace "orderId" with the actual order ID you want to process
var orderId = "order-123"; // This would typically come from a message queue or API call
var order = await daprClient.GetStateAsync<Transaction>("statestore", orderId);

if (order == null)
{
    Console.WriteLine($"Order {orderId} not found in state store. Creating sample order...");
    // Create a sample transaction if not found
    order = new Transaction(16.58m)
    {
        CustomerEmail = "customer@example.com",
        CustomerName = "Jane Smith",
        ProductName = "Wireless Headphones",
        Quantity = 2,
        OrderId = Guid.NewGuid().ToString(),
        ShippingAddress = "123 Main St, Seattle, WA 98101",
        Subtotal = 100.00m,
        Tax = 10.00m,
        ShippingCost = 5.99m,
        Total = 115.99m
    };
}

var instanceId = $"processOrder-workflow-{Guid.NewGuid().ToString()[..8]}";
await daprWorkflowClient.ScheduleNewWorkflowAsync(nameof(ProcessOrder), instanceId, order);

//Poll for status updates every second
var status = await daprWorkflowClient.GetWorkflowStateAsync(instanceId);
do
{
    Console.WriteLine($"Current status: {status.RuntimeStatus}, step: {status.ReadCustomStatusAs<string>()}");
    status = await daprWorkflowClient.GetWorkflowStateAsync(instanceId);
} while (!status.IsWorkflowCompleted);

Console.WriteLine($"Workflow completed - {status.ReadCustomStatusAs<string>()}");