//
//  ActionStateDetailView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import SwiftUI

struct ActionStateDetailView: View {
    @ObservedObject var vm: ActionStateListVM
    var actionState: ActionState
    @ObservedObject var executionVM: ActionStateExecutionVM
    var dataService: DataService
    @State var showingEditSheet = false
    @State private var showingDeleteAlert = false
    @Environment(\.dismiss) private var dismiss
    
    var triggersArray: [Trigger] {
        actionState.triggers?.allObjects as? [Trigger] ?? []
    }

    var body: some View {
        NavigationStack {
            TabView {
                
                VStack {
                    DashboardView(actionState: actionState)
                }
                .tabItem {
                    Image(systemName: "chart.xyaxis.line")
                    Text("Dashboard")
                }
                
                VStack {
                    ActionStateDetailsTab(actionState: actionState)
                }
                .tabItem {
                    Image(systemName: "book.fill")
                    Text("Details")
                }

                
                VStack {
                    ExecutionListView(actionStateListVM: vm, actionState: actionState)
                }
                .tabItem {
                    Image(systemName: "list.dash")
                    Text("Executions")
                }
                
                VStack {
                    ActionStateDetailedViewTriggers(vm: vm, actionState: actionState, executionVM: executionVM)
                        .padding()
                }
                .tabItem {
                    Image(systemName: "bolt.horizontal.circle")
                    Text("Triggers")
                }
            }
            .navigationTitle(actionState.title ?? "Untitled ActionState")
            .alert(isPresented: $showingDeleteAlert) {
                Alert(title: Text("Delete ActionState"),
                      message: Text("Are you sure you want to delete \(actionState.title ?? "this action state")?"),
                      primaryButton: .destructive(Text("Delete")) {
                        dataService.deleteActionState(actionState)
                        dismiss()  // Dismiss the detail view
                      },
                      secondaryButton: .cancel()
                )
            }
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    HStack {
                        Button(action: {
                            showingEditSheet = true
                        }, label: {
                            Image(systemName: "pencil")
                        })
                        Button(action: {
                            showingDeleteAlert = true

                            
                            print("delete pressed for \(actionState.title ?? "ActionState")")
                        }, label: {
                            Image(systemName: "trash")
                        })
                    }
                }
            }
            .sheet(isPresented: $showingEditSheet) {
                CreateEditActionStateView(vm: CreateActionStateVM(dataService: dataService, actionState: actionState))
            }
            .onReceive(NotificationCenter.default.publisher(for: .newActionStateSaved)) { _ in
                _ = dataService.fetchAllActionStates()
            }
            .onReceive(NotificationCenter.default.publisher(for: .actionStateUpdated)) { _ in
                if let id = actionState.id {
                    _ = dataService.fetchObjectByID(by: id, entityType: ActionState.self)
                }
            }

        }
    }
}



struct ActionStateDetailedViewTriggers: View {
    @ObservedObject var vm: ActionStateListVM
    var actionState: ActionState
    @ObservedObject var executionVM: ActionStateExecutionVM
    
    var triggersArray: [Trigger] {
        actionState.triggers?.allObjects as? [Trigger] ?? []
    }
    
    var executionsArray: [Execution] {
        actionState.executions?.allObjects as? [Execution] ?? []
    }
    
    let columns: [GridItem] = [
        .init(.adaptive(minimum: 50, maximum: 100))
    ]



    var body: some View {
        VStack {
            if triggersArray.isEmpty && executionsArray.isEmpty {
                Text("To execute \(actionState.title ?? "the ActionState") add a trigger")
            }
            else {
                if triggersArray.isEmpty {
                    Text("No active Triggers")
                } else {
                    LazyVGrid(columns: columns, spacing: 20) {
                        ForEach(triggersArray, id: \.self) { trigger in
                            Button(action: {
                                executionVM.startExecution(triggerID: trigger.id!)
                            }, label: {
                                Image(systemName: trigger.triggerSystemImage ?? "")
                                    .padding() // Add padding around the image
                                    .background(Color.gray.opacity(0.1)) // Add a background color
                                    .cornerRadius(8) // Round the corners
                            })
                            .buttonStyle(PlainButtonStyle())
                        }
                    }
                }
            }
        }

    }
}
