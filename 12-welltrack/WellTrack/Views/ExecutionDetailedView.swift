//
//  ExecutionDetailedView.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/23/23.
//

import SwiftUI
import MapKit

struct ExecutionDetailedView: View {
    
    let execution: ExecutionRecord
    
    @Environment(\.managedObjectContext) var moc
    @Environment(\.dismiss) var dismiss
    @State private var showingDeleteAlert = false
    
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            executionDetailHeader
            executionDetailsBody
        }
        .padding()
        .navigationTitle("\(execution.timestamp)")
        .toolbar {
            deleteButton
        }
    }
    
    private var executionDetailHeader: some View {
        VStack(alignment: .leading) {
            
            Text("Timestamp: \(execution.timestamp)")
                .font(.body)
                .foregroundColor(.secondary)
            Spacer()
        }
    }
    
    private var executionDetailsBody: some View {
        VStack {
            Text("\(execution.timestamp, style: .date) \(execution.timestamp, style: .time)")
            if execution is ExecutionString {
                let stringExecution = execution as! ExecutionString
                Text("Value: \(stringExecution.outputValue)")
            } else if execution is ExecutionNumber {
                let numberExecution = execution as! ExecutionNumber
                Text("Value: \(numberExecution.outputValue)")
            } else {
                Text("Unknown execution type")
            }
            Spacer()
        }
    }
    
    
    
    
    private var deleteButton: some View {
        Button {
            showingDeleteAlert = true
        } label : {
            Label("Delete Execution", systemImage: "trash")
        }
        .alert("Delete Execution?", isPresented: $showingDeleteAlert) {
            Button("Delete", role: .destructive, action: deleteExecution)
            Button("Cancel", role: .cancel) {}
        } message: {
            Text("Are you sure?")
        }
    }
    
    func deleteExecution() {
        moc.delete(execution)
        dismiss()
    }

}
