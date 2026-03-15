//
//  ExecutionDetailView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import SwiftUI

struct ExecutionDetailView: View {
    // Edit Execution Button
    // Delete Execution Button
    
    var execution: Execution
    
    var formattedTime: String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium // No date
        formatter.timeStyle = .medium  // Medium style for time e.g., "12:34:56 PM"
        if let date = execution.timestamp {
            return formatter.string(from: date)
        }
        return "Unknown Timestamp"
    }
    
    var body: some View {
        NavigationStack {
            List {
                
                ForEach(((execution.inputExecutions?.allObjects as? [InputExecution])?.sorted(by: { $0.order < $1.order }) ?? []), id: \.id) { inputExecution in
                    
                    Section() {
                        LabeledContent(content: {
                            if let stringInputExecution = inputExecution as? InputExecutionString {
                                Text("\(stringInputExecution.outputValue ?? "Unknown")")
                            } else if let datetimeInputExecution = inputExecution as? InputExecutionDatetime {
                                Text("\(datetimeInputExecution.outputValue ?? Date.now)")
                            } else if let doubleInputExecution = inputExecution as? InputExecutionNumber {
                                Text("\(doubleInputExecution.outputValue)")
    
                            } else if let locationInputExecution = inputExecution as? InputExecutionLocation {
                                Text("\(locationInputExecution.latitude)")
                                Text("\(locationInputExecution.longitude)")
                            }
                        }, label: {
                            if inputExecution.inputPromptBool == true {
                                Text(inputExecution.inputPromptString ?? "")
                            } else {
                                Text(inputExecution.inputTitle ?? "")
                            }
                        })
                    }
                }

            }
            
            .navigationTitle(formattedTime)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    HStack {
                        Button(action: {
                            print("edit pressed for execution")
                        }, label: {
                            Image(systemName: "pencil")
                        })
                        Button(action: {
                            print("delete pressed for execution")
                        }, label: {
                            Image(systemName: "trash")
                        })
                    }
                }
            }
        }
    }
}

// Uncomment the following section when you want to use the preview
//struct ExecutionDetailView_Previews: PreviewProvider {
//    static var previews: some View {
//        ExecutionDetailView()
//    }
//}
