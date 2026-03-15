//
//  FormattingNumbers.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/15/23.
//

import Foundation

struct FormattingHelper {
    
    // MARK: - Numbers
    
    /// Formats a Double as an Integer if it has no decimals, or keeps it as a Double if it does.
    static func formatNumber(_ value: Double) -> String {
        return value.truncatingRemainder(dividingBy: 1) == 0 ? "\(Int(value))" : "\(value)"
    }
    
    /// Removes trailing zeros from a Double.
    static func removeTrailingZeros(from value: Double) -> String {
        let formatter = NumberFormatter()
        formatter.allowsFloats = true
        formatter.minimumFractionDigits = 0
        formatter.maximumFractionDigits = 16 // Adjust as needed
        return formatter.string(from: NSNumber(value: value)) ?? "\(value)"
    }
    
    /// Formats a Double into currency format.
    static func formatAsCurrency(_ value: Double) -> String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        return formatter.string(from: NSNumber(value: value)) ?? "$\(value)"
    }
    
    // MARK: - Dates
    
    /// Shortens a date to just the month and day (e.g., "Sep 15").
    static func shortenDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "MMM dd"
        return formatter.string(from: date)
    }
    
    /// Shortens a date to just the month, day, and year (e.g., "Sep 15, 2023").
    static func shortenDateWithYear(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "MMM dd, yyyy"
        return formatter.string(from: date)
    }
    
    /// Formats a Date to show only the time.
    static func formatTime(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "h:mm a"
        return formatter.string(from: date)
    }
}
//
//// Usage examples:
//let number = 123.4567
//print(FormattingHelper.formatNumber(number))          // 123.4567
//print(FormattingHelper.removeTrailingZeros(from: 123.0)) // 123
//print(FormattingHelper.formatAsCurrency(123.4567))    // $123.46 (depends on locale)
//
//let date = Date()
//print(FormattingHelper.shortenDate(date))             // e.g., "Sep 15"
//print(FormattingHelper.shortenDateWithYear(date))     // e.g., "Sep 15, 2023"
//print(FormattingHelper.formatTime(date))              // e.g., "2:45 PM"
