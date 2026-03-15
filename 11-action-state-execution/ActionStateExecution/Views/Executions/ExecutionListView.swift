//
//  ExecutionsView.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//

import SwiftUI

struct ExecutionListView: View {
    @Environment(\.managedObjectContext) var managedObjectContext
    var actionState: ActionStateEntity
    
    var body: some View {
            List {
                Section(header:  Text("\(actionState.topic?.name ?? "") \(actionState.category ?? "")")) {
                    ForEach(Array(actionState.executions as? Set<ExecutionEntity> ?? []), id: \.self) { execution in
                        NavigationLink(destination: ExecutionDetailedView(execution: execution)) {
                            Text("\(formatDate(execution.timestamp ?? Date()))")
                        }
                    }
                }
                
                // Additional Section to display actionState attributes
                Section(header: Text("General Data")) {
                    Text("Name: \(actionState.name ?? "")")

                    Text("Category: \(actionState.category ?? "")")
                    
                    Text("Topic: \(actionState.topic?.name ?? "")")
                    ForEach(Array(actionState.tags as? Set<TagsEntity> ?? []), id: \.self) { tag in
                        Text("Tag: \(tag.name ?? "")")
                    }
                }
                
                Section(header: Text("Descriptors")) {
                    Text("Explanation: \(actionState.explanation ?? "")")
                }
                
                Section(header: Text("Collection Attributes")) {
                    
                    Text("Collect Date: \(actionState.collectDate ? "Yes" : "No")")
                    Text("Collect Location: \(actionState.collectLocation ? "Yes" : "No")")
                    Text("Collect Time: \(actionState.collectTime ? "Yes" : "No")")
                }
                

        }
        .navigationTitle(Text(actionState.name ?? "Unnamed State"))
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                NavigationLink(destination: EditActionStateView(actionState: actionState, context: self.managedObjectContext)) {
                    Text("Edit")
                }
            }
        }
        .background(Color(.systemGroupedBackground))
    }
    
    func formatDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .short
        formatter.timeStyle = .short
        return formatter.string(from: date)
    }

}
