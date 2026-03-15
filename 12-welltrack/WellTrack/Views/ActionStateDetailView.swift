//
//  ActionStateDetailView.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/15/23.
//
import SwiftUI

struct ActionStateDetailView: View {
    @Environment(\.managedObjectContext) private var moc

    @ObservedObject var actionState: ActionState
    @State private var actionStateToEdit: ActionState?
    let controller: ActionStateDataController
    
    var body: some View {
        List {
            Section("General") {
                DisclosureGroup(actionState.title) {
                    LabeledContent {
                        Text(actionState.category)
                    } label: {
                        Text("Category")
                    }
                    LabeledContent {
                        Text(actionState.dateCreated, style: .date)
                    } label: {
                        Text("Date Created")
                    }
                    
                    LabeledContent {
                        Text(actionState.dateUpdated, style: .date)
                    } label: {
                        Text("Date Updated")
                    }
                }
            }
            
            ForEach((Array(actionState.executionRecords) as! [ExecutionRecord]).sorted(by: { $0.timestamp > $1.timestamp }), id: \.self) { execution in
                
                    
                        NavigationLink(destination: ExecutionDetailedView(execution: execution)) {
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
                            }
                        }
                
                
//                NavigationLink(
//                    destination: ExecutionDetails(),
//                    label: {
//                        Text("Value: \(stringExecution.outputValue)")
//                })
//
                
//                VStack(alignment: .leading) {
//                    Text("\(execution.timestamp, style: .date) \(execution.timestamp, style: .time)")
//
//                    if execution is ExecutionString {
//                        let stringExecution = execution as! ExecutionString
//                        Text("Value: \(stringExecution.outputValue)")
//                    } else if execution is ExecutionNumber {
//                        let numberExecution = execution as! ExecutionNumber
//                        Text("Value: \(numberExecution.outputValue)")
//                    } else {
//                        Text("Unknown execution type")
//                    }
//                }
                //.log(type(of: execution))
            }




            Section("Inputs") {
                ForEach(actionState.triggers.allObjects as? [Trigger] ?? [], id: \.id) { trigger in
                    DisclosureGroup(
                        content: {
                            ForEach(trigger.childInputs?.allObjects as? [Input] ?? [].sorted(by: { $0.orderIndex < $1.orderIndex }), id: \.id) { input in
                                HStack {
                                    Text(input.title)
                                    Text(String(input.isFirst))
                                    Text(String(input.orderIndex))
                                    Spacer()
                                    Text("\(input.systemImage)")
                                }
                            }
                        },
                        label: {
                            HStack {
                                Text(Image(systemName: "\(trigger.systemImage)"))
                                Text(trigger.title)
                                Spacer()
                            }
                        }
                    )
                }
            }




        }
        .navigationTitle(actionState.title)
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button {
                    actionStateToEdit = actionState
                } label: {
                    Text("Edit")
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
    }
}

extension View {
    func log(_ items: Any...) -> some View {
        for item in items { print(item) }
        return self
    }
}






//struct ActionStateDetailView_Previews: PreviewProvider {
//    static var previews: some View {
//        ActionStateDetailView(actionState: .preview())
//    }
//}
