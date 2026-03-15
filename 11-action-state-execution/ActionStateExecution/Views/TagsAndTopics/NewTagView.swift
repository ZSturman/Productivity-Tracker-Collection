//
//  NewTagView.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//

import SwiftUI

struct NewTagView: View {
    @State private var tagName: String = ""
    @State private var tags: [String] = []
    @Environment(\.presentationMode) var presentationMode
    
    var body: some View {
            VStack {
                Form {
                    Section(header: Text("New Tag")) {
                        TextField("Tag Name", text: $tagName)
                        Button(action: {
                            self.tags.append(self.tagName)
                            self.tagName = ""
                        }) {
                            Text("Add to tag list")
                        }
                    }
                }
                List {
                    ForEach(0..<tags.count, id: \.self) { index in
                        Text("Tag: \(tags[index])")
                    }
                }
            }
            .navigationTitle("Tags")
            .navigationBarItems(trailing: Button("Done", action: {
                // Save the tags to Core Data.
                self.presentationMode.wrappedValue.dismiss()
            }))
    }
}



struct NewTagView_Previews: PreviewProvider {
    static var previews: some View {
        NewTagView()
    }
}
