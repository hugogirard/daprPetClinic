using Dapr.Workflow;
using Dapr.Client;
using Contoso.Models;

namespace Contoso.Activities;

public class NotifyWarehouseActivity : WorkflowActivity<Transaction, object?>
{
    private readonly DaprClient _daprClient;

    public NotifyWarehouseActivity(DaprClient daprClient)
    {
        _daprClient = daprClient;
    }

    /// <summary>
    /// Override to implement async (non-blocking) workflow activity logic.
    /// </summary>
    /// <param name="context">Provides access to additional context for the current activity execution.</param>
    /// <param name="input">The deserialized activity input.</param>
    /// <returns>The output of the activity as a task.</returns>
    public override async Task<object?> RunAsync(WorkflowActivityContext context, Transaction input)
    {
        // Send email to warehouse to prepare shipment
        var metadata = new Dictionary<string, string>
        {
            { "emailFrom", "orders@contoso.com" },
            { "emailTo", "warehouse@contoso.com" },
            { "subject", $"New Order to Ship - Order #{input.OrderId}" }
        };

        // Read the HTML template
        var templatePath = Path.Combine(AppContext.BaseDirectory, "Templates", "warehouse_notification_email.html");
        var htmlTemplate = await File.ReadAllTextAsync(templatePath);

        // Replace placeholders with actual values
        var htmlBody = htmlTemplate
            .Replace("{{order_id}}", input.OrderId)
            .Replace("{{customer_name}}", input.CustomerName)
            .Replace("{{product_name}}", input.ProductName)
            .Replace("{{quantity}}", input.Quantity.ToString())
            .Replace("{{order_date}}", input.OrderDate.ToString("MMMM dd, yyyy"))
            .Replace("{{shipping_address}}", input.ShippingAddress);

        // Send email using Dapr binding
        await _daprClient.InvokeBindingAsync("sendmail", "create", htmlBody, metadata);

        return null;
    }
}