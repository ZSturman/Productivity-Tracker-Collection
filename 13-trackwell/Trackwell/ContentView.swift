////
////  ContentView.swift
////  Trackwell
////
////  Created by Zachary Sturman on 8/25/23.
////
//
//import SwiftUI
//
//struct ContentView: View {
//    //@Environment(\.managedObjectContext) private var viewContext
//    //@FetchRequest(fetchRequest: ActionState.all()) private var actionStates
//    var controller = DataController.shared
//
//    var body: some View {
//        NavigationStack {
//            List {
//                Section(header: Text("Entities")) {
//                    NavigationLink("Action State", destination: ActionStateView(viewModel: ActionStateViewModel(controller: controller)))
//                    NavigationLink("Trigger", destination: TriggerView(viewModel: TriggerViewModel(controller: controller)))
//                    NavigationLink("Input", destination: InputView(viewModel: InputViewModel()))
//                    NavigationLink("Execution", destination: ExecutionView(viewModel: ExecutionViewModel(controller: controller)))
//                    NavigationLink("Input Execution", destination: InputExecutionView(viewModel: InputExecutionViewModel(controller: controller)))
//                }
//            }
//            .listStyle(GroupedListStyle())
//            .navigationBarTitle("Entities")
//            .toolbar {
//                ToolbarItem(placement: .navigationBarLeading) {
//                    Button {
//                        //actionStateToEdit = .empty(context: controller.newContext)
//                    } label: {
//                        Image(systemName: "plus")
//                            .font(.title2)
//                    }
//                }
//            }
//        }
//    }
//}
//
//
//struct ContentView_Previews: PreviewProvider {
//    static var previews: some View {
//        ContentView()
//    }
//}
