import SwiftUI
import CoreData

struct AddActionStateFormView: View {
    @StateObject var actionStateViewModel: ActionStateViewModel
    @StateObject var topicListViewModel: TopicViewModel
    
    
    @Environment(\.dismiss) var dismiss
    @State private var selectedTopicId: UUID?
    @State private var isShowingManualInputForm = false
    
    init(moc: NSManagedObjectContext) {
        _actionStateViewModel = StateObject(wrappedValue: ActionStateViewModel(moc: moc))
        _topicListViewModel = StateObject(wrappedValue: TopicViewModel(moc: moc))
    }


    var body: some View {
        Form {
            Section {
                Picker("Type", selection: $actionStateViewModel.type) {
                    ForEach(actionStateViewModel.types, id: \.self) {
                        Text($0)
                    }
                }
                .pickerStyle(SegmentedPickerStyle())
            }
            
            Section {
                TextField("Title of \(actionStateViewModel.type)", text: $actionStateViewModel.name)
                TextEditor(text: $actionStateViewModel.explanation)
            }
            
            
            Section {
                Picker("Topic", selection: $selectedTopicId) {
                    ForEach(topicListViewModel.topics, id: \.id) { topic in
                        Text(topic.name ?? "Untitled Topic").tag(topic.id)
                    }
                }
            }

            
            Section {
                Toggle(isOn: $actionStateViewModel.collectDate) {
                    Text("Collect Date")
                }
                Toggle(isOn: $actionStateViewModel.collectTime) {
                    Text("Collect Time")
                }
                Toggle(isOn: $actionStateViewModel.collectLocation) {
                    Text("Collect Location")
                }
            }
            
            Section {
                Button("Add Manual Input") {
                    isShowingManualInputForm = true
                    actionStateViewModel.isManualInputButtonPressed = true
                }

            }
        }
        .sheet(isPresented: $isShowingManualInputForm) {
            AddManualInputFormView()
        }


        .navigationTitle("New ActionState")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button("Save") {
                    actionStateViewModel.addNewItem()
                    dismiss()
                }
            }
        }
    }
}
