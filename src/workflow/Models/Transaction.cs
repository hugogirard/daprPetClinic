namespace Contoso.Models;

public record Transaction(decimal Value)
{
    public Guid CustomerId { get; init; } = Guid.NewGuid();
    public string CustomerEmail { get; init; } = string.Empty;
    public string CustomerName { get; init; } = string.Empty;
    public string ProductName { get; init; } = string.Empty;
    public int Quantity { get; init; } = 1;
    public string OrderId { get; init; } = string.Empty;
    public string ShippingAddress { get; init; } = string.Empty;
    public DateTime OrderDate { get; init; } = DateTime.UtcNow;
    public decimal Subtotal { get; init; }
    public decimal Tax { get; init; }
    public decimal ShippingCost { get; init; }
    public decimal Total { get; init; }
}