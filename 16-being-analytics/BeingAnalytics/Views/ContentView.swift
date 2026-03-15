//
//  ContentView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import SwiftUI

struct ContentView: View {
    
    @ObservedObject var dataService: DataService
    @ObservedObject var actionStateListVM: ActionStateListVM
    @State var showingCreateSheet = false
    @ObservedObject var actionStateExecutionVM: ActionStateExecutionVM

    
    init() {
        let service = DataService()
        self.dataService = service
        self.actionStateListVM = ActionStateListVM(dataService: service)
        self.actionStateExecutionVM = ActionStateExecutionVM(dataService: service)
    }
    
    var body: some View {
        NavigationStack {
                ZStack {
                    if actionStateListVM.actionStates.isEmpty {
                        NoActionStatesView()
                    } else {
                        ActionStateListView(vm: actionStateListVM, executionVM: actionStateExecutionVM, dataService: dataService)
                    }
                    
                }
                .navigationTitle("BeingAnalytics")
                .toolbar {
                    ToolbarItem(placement: .navigationBarLeading) {
                        Button(action: {
                            showingCreateSheet.toggle()
                        }, label: {
                            Image(systemName: "plus")
                        })
                    }
                    ToolbarItem(placement: .navigationBarTrailing) {
                        Menu {
                            Section(header: Text("Filter")) {
                                Button(action: { actionStateListVM.searchConfig.filter = .all }) {
                                    HStack {
                                        Text("All")
                                        Spacer()
                                        if actionStateListVM.searchConfig.filter == .all {
                                            Image(systemName: "checkmark")
                                        }
                                    }
                                }
                                
                                Button(action: { actionStateListVM.searchConfig.filter = .action }) {
                                    HStack {
                                        Text("Action")
                                        Spacer()
                                        if actionStateListVM.searchConfig.filter == .action {
                                            Image(systemName: "checkmark")
                                        }
                                    }
                                }

                                Button(action: { actionStateListVM.searchConfig.filter = .state }) {
                                    HStack {
                                        Text("State")
                                        Spacer()
                                        if actionStateListVM.searchConfig.filter == .state {
                                            Image(systemName: "checkmark")
                                        }
                                    }
                                }
                            }

                            Section(header: Text("Date Updated")) {
                                Button(action: { actionStateListVM.sort = .asc }) {
                                    HStack {
                                        Label("Asc", systemImage: "arrow.up")
                                        Spacer()
                                        if actionStateListVM.sort == .asc {
                                            Image(systemName: "checkmark")
                                        }
                                    }
                                }

                                Button(action: { actionStateListVM.sort = .desc }) {
                                    HStack {
                                        Label("Desc", systemImage: "arrow.down")
                                        Spacer()
                                        if actionStateListVM.sort == .desc {
                                            Image(systemName: "checkmark")
                                        }
                                    }
                                }
                            }

                        } label: {
                            Image(systemName: "ellipsis")
                                .symbolVariant(.circle)
                                .font(.title2)
                        }
                    }
                }
                .sheet(isPresented: $showingCreateSheet) {
                    CreateEditActionStateView(vm: CreateActionStateVM(dataService: dataService))
                }

                .sheet(isPresented: actionStateExecutionVM.isInputSheetPresented, onDismiss: {
                    if let executionVM = actionStateExecutionVM.executionVM {
                         executionVM.checkInputExecution()
                     } else {
                         // Handle the case where executionVM is nil, if necessary
                         print("Warning: executionVM is nil.")
                     }
                }, content: {
                    InputSheetView(actionStateExecutionVM: actionStateExecutionVM)
                        .id(UUID())
                        .presentationDetents([.medium, .large])
                        .interactiveDismissDisabled()
                        .presentationBackground(.thinMaterial)
                })
                .onChange(of: actionStateListVM.searchConfig) { _ in
                    actionStateListVM.filterAndSortActionStates()
                }
                .onChange(of: actionStateListVM.sort) { _ in
                    actionStateListVM.filterAndSortActionStates()
                }
        }
        .onReceive(NotificationCenter.default.publisher(for: .newActionStateSaved)) { _ in
            _ = dataService.fetchAllActionStates()
        }
    }
}


#Preview {
    ContentView()
}
