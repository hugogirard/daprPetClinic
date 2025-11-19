using Dapr.Workflow;
using Dapr.Client;
using Contoso.Models;

namespace Contoso.Activities;

public class ProcessPaymentActivity : WorkflowActivity<Transaction, object?>
{
    private readonly DaprClient _daprClient;

    public ProcessPaymentActivity(DaprClient daprClient)
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
        // Process payment and send customer invoice email
        var metadata = new Dictionary<string, string>
        {
            { "emailFrom", "orders@contoso.com" },
            { "emailTo", input.CustomerEmail },
            { "subject", $"Order Confirmation - Order #{input.OrderId}" }
        };

        // Read the HTML template
        var templatePath = Path.Combine(AppContext.BaseDirectory, "Templates", "order_confirmation_email.html");
        var htmlTemplate = await File.ReadAllTextAsync(templatePath);

        // Replace placeholders with actual values
        var htmlBody = htmlTemplate
            .Replace("{{customer_name}}", input.CustomerName)
            .Replace("{{order_id}}", input.OrderId)
            .Replace("{{order_date}}", input.OrderDate.ToString("MMMM dd, yyyy"))
            .Replace("{{product_name}}", input.ProductName)
            .Replace("{{quantity}}", input.Quantity.ToString())
            .Replace("{{shipping_address}}", input.ShippingAddress)
            .Replace("{{subtotal}}", input.Subtotal.ToString("F2"))
            .Replace("{{tax}}", input.Tax.ToString("F2"))
            .Replace("{{shipping_cost}}", input.ShippingCost.ToString("F2"))
            .Replace("{{total}}", input.Total.ToString("F2"));

        // Send email using Dapr binding
        await _daprClient.InvokeBindingAsync("sendmail", "create", htmlBody, metadata);

        return null;
    }
}