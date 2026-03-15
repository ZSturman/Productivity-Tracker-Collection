//
//  ExecutionRowView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//
import SwiftUI

struct ExecutionRowView: View {
    
    var execution: Execution

    var formattedTime: String {
        let formatter = DateFormatter()
        formatter.dateStyle = .none  // No date
        formatter.timeStyle = .medium  // Medium style for time e.g., "12:34:56 PM"
        if let date = execution.timestamp {
            return formatter.string(from: date)
        }
        return "No Time"
    }

    var body: some View {
        NavigationStack {
            VStack {
                NavigationLink(destination: ExecutionDetailView(execution: execution), label: {
                    LabeledContent(content: {
                        Text("\(execution.outputValue ?? "")")
                    }, label: {
                        Text(formattedTime)
                    })
                })
            }
        }
    }
}
