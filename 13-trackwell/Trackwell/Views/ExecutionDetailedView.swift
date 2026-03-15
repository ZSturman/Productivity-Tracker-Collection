//
//  ExecutionDetailedView.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/26/23.
//



import SwiftUI

struct ExecutionDetailedView: View {
    let execution: Execution
    
    var body: some View {
        NavigationStack {
            List {
                Section(header: Text("Execution Details")) {
                    Text("Trigger: \(execution.trigger.type.rawValue)")
                    Text("Timestamp: \(execution.timestamp)")
                }
                
                Section(header: Text("Input Executions")) {
                    ForEach(execution.inputExecutions.sorted(by: { $0.order < $1.order }), id: \.id) { inputExecution in
                        Text("\(inputExecution.title) (Order: \(inputExecution.order))")
                    }
                    .onAppear {
                        print("Rendering InputExecutions for execution of trigger: \(execution.trigger.type.rawValue)")
                    }
                }

            }
        }
        .navigationTitle("Timestamp: \(execution.timestamp)")
    }
    
}
