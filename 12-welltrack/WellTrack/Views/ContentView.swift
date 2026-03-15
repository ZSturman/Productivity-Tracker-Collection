//
//  ContentView.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/15/23.
//

import SwiftUI

struct SearchConfig: Equatable {
    enum Filter {
        case all, action, state
    }
    var query: String = ""
    var filter: Filter = .all
}

enum Sort {
    case asc, desc
}

struct ContentView: View {
    @FetchRequest(fetchRequest: ActionState.all()) private var actionStates
    
    @State private var actionStateToEdit: ActionState?
    @State private var searchConfig: SearchConfig = .init()

    @State private var sort: Sort = .desc
    var controller = ActionStateDataController.shared
    
    var body: some View {
        NavigationStack {
            ZStack {
                if actionStates.isEmpty {
                    NoActionStateView()
                } else {
                    List {
                        ForEach(actionStates){ actionState in
                            ZStack(alignment: .leading) {
                                NavigationLink(destination: ActionStateDetailView(actionState: actionState, controller: controller)) {
                                    EmptyView()
                                }
                                .opacity(0)
                                
                                ActionStateRowView(vm: .init(controller: controller, actionState: actionState))

                                    .swipeActions(allowsFullSwipe: true) {
                                        Button(role: .destructive) {
                                            do {
                                                try controller.delete(actionState, in: controller.newContext)
                                            } catch {
                                                print(error)
                                            }
                                        } label: {
                                            Label("Delete", systemImage: "trash")
                                        }
                                        .tint(.red)
                                        
                                        Button {
                                            actionStateToEdit = actionState
                                        } label: {
                                            Label("Edit", systemImage: "pencil")
                                        }
                                        .tint(.orange)
                                    }
                            }
                        }
                    }
                }
            }
            .searchable(text: $searchConfig.query)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button {
                        actionStateToEdit = .empty(context: controller.newContext)
                    } label: {
                        Image(systemName: "plus")
                            .font(.title2)
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    
                    Menu {

                        Section(header: Text("Filter")) {
                            Button(action: { searchConfig.filter = .all }) {
                                HStack {
                                    Text("All")
                                    Spacer()
                                    if searchConfig.filter == .all {
                                        Image(systemName: "checkmark")
                                    }
                                }
                            }
                            
                            Button(action: { searchConfig.filter = .action }) {
                                HStack {
                                    Text("Action")
                                    Spacer()
                                    if searchConfig.filter == .action {
                                        Image(systemName: "checkmark")
                                    }
                                }
                            }

                            Button(action: { searchConfig.filter = .state }) {
                                HStack {
                                    Text("State")
                                    Spacer()
                                    if searchConfig.filter == .state {
                                        Image(systemName: "checkmark")
                                    }
                                }
                            }
                        }

                        Section(header: Text("Date Updated")) {
                            Button(action: { sort = .asc }) {
                                HStack {
                                    Label("Asc", systemImage: "arrow.up")
                                    Spacer()
                                    if sort == .asc {
                                        Image(systemName: "checkmark")
                                    }
                                }
                            }

                            Button(action: { sort = .desc }) {
                                HStack {
                                    Label("Desc", systemImage: "arrow.down")
                                    Spacer()
                                    if sort == .desc {
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
            .sheet(item: $actionStateToEdit,
                   onDismiss: {
                actionStateToEdit = nil
            }, content: { actionState in
                NavigationStack {
                    CreateEditActionState(vm: .init(controller: controller, actionState: actionState))
                }
            })
            .navigationTitle("ActionStates")
            .onChange(of: searchConfig) { newConfig in
                actionStates.nsPredicate = ActionState.filter(with: newConfig)
            }
            .onChange(of: sort) { newSort in
                actionStates.nsSortDescriptors = ActionState.sort(order: newSort)
            }
        }
    }
}





struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        let preview = ActionStateDataController.shared
        ContentView(controller: preview)
            .environment(\.managedObjectContext, preview.viewContext)
            .previewDisplayName("ActionStates With Data")
            .onAppear { ActionState.makePreview(count: 10, in: preview.viewContext) }
        
        let emptyPreview = ActionStateDataController.shared
        ContentView(controller: emptyPreview)
            .environment(\.managedObjectContext, emptyPreview.viewContext)
            .previewDisplayName("ActionStates With No Data")
    }
}

