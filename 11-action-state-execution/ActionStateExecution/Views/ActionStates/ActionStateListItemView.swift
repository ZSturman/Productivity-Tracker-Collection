//
//  ActionStateListItemView.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/2/23.
//

import CoreData
import SwiftUI
struct ActionStateListItemView: View {
    var actionState: ActionStateEntity
    @Environment(\.managedObjectContext) var managedObjectContext

    @StateObject var executionViewModel: ExecutionViewModel
    
    init(actionState: ActionStateEntity, managedObjectContext: NSManagedObjectContext) {
        self.actionState = actionState
        self._executionViewModel = StateObject(wrappedValue: ExecutionViewModel(context: managedObjectContext))
    }
    
    var body: some View {
            HStack {
                Button(action: {
                    let sortedFields = actionState.fields?.sorted(by: { field1, field2 in
                        guard let field1 = field1 as? FieldEntity, let field2 = field2 as? FieldEntity else { return false }
                        return field1.order < field2.order
                    }) as? [FieldEntity] ?? []
                    
                    executionViewModel.executeActionState(actionState: actionState, fields: sortedFields)
                }) {
                    Text("Execute")
                        .padding(.horizontal, 16)
                        .padding(.vertical, 10)
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .shadow(color: .gray, radius: 2, x: 0, y: 2)
                
                Spacer()
                
                NavigationLink(destination: ExecutionListView(actionState: actionState)) {
                    HStack {
                        Text(actionState.name ?? "Unnamed State")
                            .fontWeight(.semibold)
                        Spacer()
                        
                        if let executionSet = actionState.executions as? Set<ExecutionEntity>,
                           let lastExecution = executionSet.sorted(by: { $0.timestamp ?? Date() < $1.timestamp ?? Date() }).last {
                            Text("Last Executed: \(formatDate(lastExecution.timestamp ?? Date()))")
                                .font(.footnote)
                                .foregroundColor(.gray)
                        }
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(10)
                }
                .buttonStyle(PlainButtonStyle())
                .shadow(color: .gray, radius: 2, x: 0, y: 2)
            }
            .padding()
            .sheet(isPresented: $executionViewModel.isSheetShowing) {
                ExecutionInputView(viewModel: executionViewModel)
            }
    }
    
    func formatDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .short
        formatter.timeStyle = .short
        return formatter.string(from: date)
    }
}

