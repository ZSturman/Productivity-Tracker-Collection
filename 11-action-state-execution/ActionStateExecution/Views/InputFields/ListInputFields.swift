//
//  ListInputFields.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/1/23.
//

import SwiftUI

struct ListInputFields: View, FieldCreator {
    @State private var showNewList = false
    @Environment(\.managedObjectContext) var managedObjectContext
    @FetchRequest(entity: ListEntity.entity(), sortDescriptors: []) var lists: FetchedResults<ListEntity>

    @Binding var selection: String
    @Binding var listSelectMultiple: Bool
    @Binding var listAddAtExecution: Bool
    @Binding var listSelectedList: UUID?
    @State private var selectedListUUID: UUID?
    
    var body: some View {
        Section(header: Text("\(selection)")) {
            Toggle("Select Multiple", isOn: $listSelectMultiple)
            Toggle("Add at execution", isOn: $listAddAtExecution)
        }

        Section(header: Text("List of Lists"), footer: Text("Select a list or create a new one")) {
            List {
                ForEach(lists, id: \.self) { list in
                    HStack {
                        Button(action: {
                            self.selectedListUUID = list.id
                            self.listSelectedList = list.id
                        }) {
                            Image(systemName: self.selectedListUUID == list.id ? "largecircle.fill.circle" : "circle")
                                .resizable()
                                .frame(width: 20, height: 20)
                                .foregroundColor(.blue)
                        }
                        .buttonStyle(PlainButtonStyle())

                        
                        NavigationLink(destination: ListItemView(list: list)) {
                            Text(list.name ?? "")
                        }
                    }
                }
                HStack {
                    NavigationLink(destination: NewListView()) {
                        Text("Create new list")
                    }
                    
                }
            }
        }
    }
    
    func createField(name: String, prompt: String) -> InputFieldVariables {
        InputFieldVariables(name: name,
              prompt: prompt,
              selection: selection,
              listSelectMultiple: listSelectMultiple,
              listAddAtExecution: listAddAtExecution,
              listSelectedList: listSelectedList
        )
    }
    
    func populateField(with field: InputFieldVariables) {
        self.selection = field.selection
        self.listSelectMultiple = field.listSelectMultiple ?? false
        self.listAddAtExecution = field.listAddAtExecution ?? false
        self.listSelectedList = field.listSelectedList
    }
}

struct RadioButtonGroups: View {
    @Binding var selectedId: UUID?
    let id: UUID?
    
    var body: some View {
        Button(action: {
            self.selectedId = self.id
        }) {
            HStack {
                if self.selectedId == self.id {
                    Image(systemName: "largecircle.fill.circle")
                } else {
                    Image(systemName: "circle")
                }
            }
        }
        .foregroundColor(Color(UIColor.label))
    }
}
